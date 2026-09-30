# -*- coding: utf-8 -*-
"""S3.5b 判读（预注册口径）：主门 = g22_mean_latest 配对差 >2SD 且 ≥6/8 正。"""
import csv
from statistics import median, stdev

rows = []
for t in "abcd":
    rows.extend(csv.DictReader(open(f"_rerun_logs/s35b/s35b_{t}.csv", encoding="utf-8")))

seeds = sorted({int(r["seed"]) for r in rows})
runs = {(int(r["seed"]), r["arm"]) for r in rows}
print(f"完整性: {len(seeds)} seed × 2 臂 = {len(runs)} run（预期 16）{'✅' if len(runs)==16 else '🔴'}")

term = {(int(r["seed"]), r["arm"]): r for r in rows if r["tick"].strip() == "2000"}

deltas, off_latest = [], []
for s in seeds:
    on, off = term.get((s, "mem_on")), term.get((s, "mem_off"))
    if on and off:
        dv = float(on["g22_mean_latest"]) - float(off["g22_mean_latest"])
        deltas.append((s, dv))
        off_latest.append(float(off["g22_mean_latest"]))

sd_null = stdev(off_latest)
med = median([d for _, d in deltas])
pos = sum(1 for _, d in deltas if d > 0)
print(f"\n=== 主门 A：g22_latest 配对差（on−off）@2000 ===")
print(f"正: {pos}/{len(deltas)}（通过线 ≥6/8）| 中位差: {med:+.4f}")
print(f"SD_null（off 臂 latest 种子间 SD）: {sd_null:.4f} | 2×SD_null = {2*sd_null:.4f}")
ok = (pos >= 6) and (med > 2 * sd_null)
print(f"判定: {'✅ 通过' if ok else '❌ 未通过'}（条件：≥6/8 正 且 中位差>2SD）")

# 支持 B：on 臂单调性
mono = 0
for s in seeds:
    on = term[(s, "mem_on")]
    v = [float(on.get(f"g22_mean_gen{i}", "nan")) for i in range(3)] + [float(on.get("g22_mean_gen3p", "nan"))]
    v = [x for x in v if x == x]  # 去掉 NaN
    if len(v) >= 2 and all(v[i] < v[i+1] for i in range(len(v)-1)):
        mono += 1
print(f"\n=== 支持 B：on 臂代际单调性（gen0<gen1<gen2<gen3+）===")
print(f"单调 seed 数: {mono}/8（参考线 ≥5）")

# 支持 C：稀释量化
dil = []
for s in seeds:
    for arm in ("mem_on", "mem_off"):
        r = term[(s, arm)]
        dl = float(r["g22_mean_latest"]) - float(r["g22_mean"])
        if dl == dl:
            dil.append(dl)
print(f"\n=== 支持 C：latest − all 稀释量化 ===")
print(f"中位差: {median(dil):+.4f}（>0 = 全群均值低估新生代）")

print(f"\n=== 逐 seed 明细 ===")
print(f"{'seed':>5} {'Δlatest':>9} {'on_latest':>9} {'off_latest':>10} {'on_gen0':>8} {'on_max_gen':>10}")
for s, d in deltas:
    on = term[(s, "mem_on")]
    print(f"{s:>5} {d:>+9.4f} {float(on['g22_mean_latest']):>9.4f} {float(term[(s,'mem_off')]['g22_mean_latest']):>10.4f} {float(on['g22_mean_gen0']):>8.4f} {on['max_gen']:>10}")
