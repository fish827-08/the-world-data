#!/usr/bin/env python3.12
"""迁徙探针 v2 —— 检验"种群质心纬度是否跟随季节资源带移动"。

判据（13.7 设计稿 §2.2）：
  centroid_lat(t) = 种群质心纬度（按 cos(lat) 面积加权）
  band_lat(t)     = 该 tick 资源最富的纬度带中心
  有迁徙 ⇔ corr(centroid_lat(t), band_lat(t)) 显著 > 0 且滞后小
  无迁徙 ⇔ 相关不显著（阴性也要过世代门）

v2 增强：同时记录 **三种纬度带**，把"季节驱动"与"储量滞后"分开：
  - band_env : 光照/温度带中心（纯季节信号，生物应跟随的"真值"）  ← v2 新增
  - band_res : 资源**存量**带中心（受 storage effect 滞后/平滑）    ← 原判据
  - centroid : 种群质心
  ⇒ 可判读"生物跟的是光照带还是存量带"（若跟光照 ⇒ 主动迁徙；若只跟存量 ⇒ 被动漂移）

用法：
  python3.12 run_migration.py --seed 42 --tilt 23.44 --season-period 6000 \
      --ticks 18000 --temp-sensitivity 6.0 --out /workspace/mig_s42.csv
"""
import argparse
import importlib.util
import json
import math

import numpy as np

from simulation.genes import Gene


def install_light_regrowth(light_k=1.0, normalize=True):
    """把 ResourceField 再生改成「温度 × 光照」⇒ 让食物带随季节移动。

    ⚠️ __slots__ ⇒ 改类方法（原型阶段）。
    """
    from world.resource_field import ResourceField
    if not hasattr(ResourceField, "_orig_regrowth_amount"):
        ResourceField._orig_regrowth_amount = ResourceField._regrowth_amount

    def new_regrowth(self, tick):
        lt = self.lt
        allc = np.arange(self.world.n_cells, dtype=np.int64)
        temps = lt.temperature(allc, tick)
        tf = np.power(np.clip((temps + 20.0) / 20.0, 0.0, 1.0), 1.0)
        ill = lt.illumination(allc, tick)
        lf = np.power(np.clip(ill, 0.0, 1.0), light_k)
        if normalize:
            m = float(lf.mean())
            if m > 1e-9:
                lf = lf / m
        g = self.regrowth_rate * tf * lf
        if self.distribution == "patchy" and self._patch_mask is not None:
            g = np.where(self._patch_mask,
                         g * self._patch_regrowth_mult,
                         g * self._bg_regrowth_mult)
        return g

    ResourceField._regrowth_amount = new_regrowth

A4 = "/tmp/tw/experiments/a4_verify_capacity.py"


def load_build():
    spec = importlib.util.spec_from_file_location("a4mod", A4)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def make_engine(seed, ticks, tilt_deg, season_period, k=0.0,
                max_count=3240, temp_sensitivity=None):
    mod = load_build()
    kw = dict(
        mode="on", codebook=True, seed=seed, ticks=ticks,
        max_count=max_count, soft_cap_target=0.6, distribution="patchy",
        energy_cap=True, signal_alphabet="16", forage_tradeoff_k=float(k),
        measure=False,
    )
    if tilt_deg is not None:
        kw["tilt_deg"] = float(tilt_deg)
        kw["season_period"] = int(season_period)
    eng = mod.build(**kw)
    cfg = eng.config
    if temp_sensitivity is not None and \
            float(cfg.resources.temp_sensitivity) != float(temp_sensitivity):
        cfg.resources.temp_sensitivity = float(temp_sensitivity)
        from simulation.sphere_engine import SphereEngine
        eng = SphereEngine(cfg)
    return eng


def alive_count(eng):
    """存活个体数（不用 `_pop_n` 惰性字段）。"""
    return int((eng._genes[:, Gene.AGGRESSION] > 0).sum())


def lat_centroid(eng):
    alive = eng._genes[:, Gene.AGGRESSION] > 0
    n = int(alive.sum())
    if n <= 0:
        return None
    flat = eng._flat[alive]
    rows, _ = eng.world.flat_to_rc(flat)
    lat = eng.world.latitude_of(rows)
    w = np.maximum(np.cos(lat), 1e-6)
    return float((lat * w).sum() / w.sum())


def band_lat_res(eng):
    """资源存量带中心。"""
    stock = np.asarray(eng.resources.snapshot(), dtype=float)
    if stock.ndim == 1:
        stock = stock.reshape(eng.world.rows, eng.world.cols)
    lat_rows = eng.world.latitude_of(np.arange(stock.shape[0]))
    row_stock = stock.sum(axis=1)
    if row_stock.sum() <= 1e-12:
        return None
    w = np.maximum(row_stock, 0.0) * np.cos(lat_rows)
    if w.sum() <= 1e-12:
        return None
    return float((lat_rows * w).sum() / w.sum())


def band_lat_env(eng):
    """光照带中心（纯季节信号）。"""
    eng.light._ensure_cache(int(eng.tick))
    ill = np.asarray(eng.light._cache_illum_all, dtype=float)
    rows, cols = eng.world.rows, eng.world.cols
    if ill.ndim == 1:
        ill = ill.reshape(rows, cols)
    lat_rows = eng.world.latitude_of(np.arange(rows))
    row_ill = ill.sum(axis=1)
    if row_ill.sum() <= 1e-12:
        return None
    w = row_ill * np.cos(lat_rows)
    if w.sum() <= 1e-12:
        return None
    return float((lat_rows * w).sum() / w.sum())


def best_lag_corr(a, b, max_lag=10):
    """扫描 corr(a[t+lag], b[t])，返回 (best_corr, best_lag, corr_at_0, curve)。"""
    curve = {}
    best, bl = -2.0, 0
    for lag in range(-max_lag, max_lag + 1):
        if lag >= 0:
            x, y = a[lag:], (b[:len(b) - lag] if lag else b)
        else:
            x, y = a[:lag], b[-lag:]
        if len(x) < 4 or x.std() < 1e-9 or y.std() < 1e-9:
            continue
        c = float(np.corrcoef(x, y)[0, 1])
        curve[lag] = round(c, 4)
        if c > best:
            best, bl = c, lag
    c0 = None
    if a.std() > 1e-9 and b.std() > 1e-9:
        c0 = round(float(np.corrcoef(a, b)[0, 1]), 4)
    return (None if best < -1.5 else round(best, 4)), bl, c0, curve


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--tilt", type=float, default=None, help="度；None=无季节")
    ap.add_argument("--season-period", type=int, default=6000)
    ap.add_argument("--ticks", type=int, default=18000)
    ap.add_argument("--log-interval", type=int, default=250)
    ap.add_argument("--k", type=float, default=0.0)
    ap.add_argument("--temp-sensitivity", type=float, default=None)
    ap.add_argument("--light-regrowth", action="store_true",
                    help="光驱动再生：食物带随季节移动（重大机制改动）")
    ap.add_argument("--light-k", type=float, default=1.0)
    ap.add_argument("--light-normalize", action="store_true", default=None,
                    help="光照因子按全球均值归一化")
    ap.add_argument("--engine-mechanism", action="store_true",
                    help="用引擎正式字段 resources.light_sensitivity（R196 已下沉）"
                         "而非猴子补丁 —— 应与 --light-regrowth 结果一致")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    eng = make_engine(args.seed, args.ticks, args.tilt, args.season_period,
                      args.k, temp_sensitivity=args.temp_sensitivity)
    if args.light_regrowth:
        if args.engine_mechanism:
            # R196 正式路径：改 config → 重建引擎（引擎构造期透传到 ResourceField）
            from simulation.sphere_engine import SphereEngine
            cfg = eng.config
            cfg.resources.light_sensitivity = float(args.light_k)
            if args.light_normalize:
                cfg.resources.light_normalize = True
            eng = SphereEngine(cfg)
        else:
            install_light_regrowth(light_k=args.light_k,
                                   normalize=bool(args.light_normalize))
    mech = ("engine" if args.engine_mechanism else "monkeypatch") \
        if args.light_regrowth else "none"
    print(f"[init] seed={args.seed} tilt={args.tilt} P={args.season_period} "
          f"ticks={args.ticks} season_on={eng.light._season_on} "
          f"temp_sens={eng.config.resources.temp_sensitivity} "
          f"light_regrowth={args.light_regrowth} light_k={args.light_k} "
          f"mechanism={mech} "
          f"rust={eng._use_sim_core}", flush=True)

    rows = []
    for t in range(1, args.ticks + 1):
        eng.step()
        if t % args.log_interval == 0:
            n = alive_count(eng)
            cl = lat_centroid(eng)
            br = band_lat_res(eng)
            be = band_lat_env(eng)
            alive = eng._genes[:, Gene.AGGRESSION] > 0
            g = eng._genes[alive, Gene.AGGRESSION] if n > 0 else np.zeros(0)
            rows.append([t, n,
                         "" if cl is None else f"{math.degrees(cl):.4f}",
                         "" if br is None else f"{math.degrees(br):.4f}",
                         "" if be is None else f"{math.degrees(be):.4f}",
                         f"{float(g.mean()):.6f}" if n > 0 else ""])
            if t % (args.log_interval * 8) == 0:
                print(f"  t={t} N={n} centroid={rows[-1][2]} "
                      f"band_res={rows[-1][3]} band_env={rows[-1][4]}", flush=True)
            if n == 0:
                print(f"[warn] t={t} 灭绝", flush=True)
                break

    with open(args.out, "w") as f:
        f.write("tick,N,centroid_lat_deg,band_res_deg,band_env_deg,g16_mean\n")
        for r in rows:
            f.write(",".join(str(x) for x in r) + "\n")

    def col(i):
        return np.array([float(r[i]) for r in rows if r[i] != ""])

    cl = col(2)
    br = col(3)
    be = col(4)

    def summ_pair(a, b):
        if len(a) < 4 or a.std() < 1e-9 or b.std() < 1e-9:
            return {"best_corr": None, "best_lag": None, "corr0": None, "curve": {}}
        bc, bl, c0, curve = best_lag_corr(a, b)
        return {"best_corr": bc, "best_lag": bl, "corr0": c0, "curve": curve}

    s_res = summ_pair(cl, br)      # 质心 vs 资源存量带（原判据）
    s_env = summ_pair(cl, be)      # 质心 vs 光照带（季节真值）

    summary = {
        "seed": args.seed, "tilt_deg": args.tilt,
        "season_period": args.season_period, "ticks_target": args.ticks,
        "temp_sensitivity": float(eng.config.resources.temp_sensitivity),
        "season_on": bool(eng.light._season_on),
        "final_tick": rows[-1][0] if rows else 0,
        "final_N": rows[-1][1] if rows else 0,
        "centroid_vs_band_res": s_res,
        "centroid_vs_band_env": s_env,
        "band_res_series": [r[3] for r in rows],
        "band_env_series": [r[4] for r in rows],
        "centroid_series": [r[2] for r in rows],
        "N_series": [r[1] for r in rows],
        "out": args.out,
    }
    with open(args.out.replace(".csv", ".summary.json"), "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("\n=== 迁徙判据 ===", flush=True)
    print(f"final_N = {summary['final_N']}")
    print(f"[原判据] corr(centroid, band_res): "
          f"best={s_res['best_corr']} @lag={s_res['best_lag']}  (corr0={s_res['corr0']})")
    print(f"[季节真值] corr(centroid, band_env): "
          f"best={s_env['best_corr']} @lag={s_env['best_lag']}  (corr0={s_env['corr0']})")
    print(f"band_res sweep = {br.max()-br.min():.3f}°  "
          f"(std={br.std():.4f})" if len(br) else "")
    print(f"band_env sweep = {be.max()-be.min():.3f}°  "
          f"(std={be.std():.4f})" if len(be) else "")
    if s_res["curve"]:
        print(f"band_res lag curve: {s_res['curve']}")
    if s_env["curve"]:
        print(f"band_env lag curve: {s_env['curve']}")


if __name__ == "__main__":
    main()
