# -*- coding: utf-8 -*-
"""S3.5 判读（R275 预注册口径）：g22 选择压。
主门 A = g22_mean 配对差（on−off）@t=2000；判定 = |中位差| > 2×SD_null（自校准）。
附：置换检验 p 值（seed 内臂标签置换 10000 次）+ 轨迹。
"""
import csv
import random
from statistics import median, stdev

rows = []
for t in "abcd":
    rows.extend(csv.DictReader(open(f"_rerun_logs/s35/s35_{t}.csv", encoding="utf-8")))

seeds = sorted({int(r["seed"]) for r in rows})
runs = {(int(r["seed"]), r["arm"]) for r in rows}
print(f"完整性: {len(seeds)} seed × 2 臂 = {len(runs)} run（预期 32）{'✅' if len(runs) == 32 else '🔴'}")

term = {(int(r["seed"]), r["arm"]): r for r in rows if r["tick"].strip() == "2000"}

deltas, off_vals, on_vals = [], [], []
for s in seeds:
    on, off = term.get((s, "mem_on")), term.get((s, "mem_off"))
    if on and off:
        do = float(on["g22_mean"]); df = float(off["g22_mean"])
        deltas.append((s, do - df)); on_vals.append(do); off_vals.append(df)

med = median([d for _, d in deltas])
sd_null = stdev(off_vals)          # 自校准：off 臂（纯漂变对照）种子间 SD
neg = sum(1 for _, d in deltas if d < 0); pos = sum(1 for _, d in deltas if d > 0)

print(f"\n=== 主门 A：g22_mean 配对差（on−off）@t=2000 ===")
print(f"seed 数: {len(deltas)} | 正: {pos} / 负: {neg}")
print(f"中位差: {med:+.5f} | 均值: {sum(d for _, d in deltas)/len(deltas):+.5f}")
print(f"SD_null（off 臂种子间 SD）: {sd_null:.5f} | 2×SD_null = {2*sd_null:.5f}")
verdict = "显形" if abs(med) > 2 * sd_null else "未达线"
print(f"判定: |中位差| = {abs(med):.5f} vs 2SD = {2*sd_null:.5f} ⇒ **{verdict}**（方向: {'正=记忆被青睐' if med > 0 else '负=成本主导'}）")

# 置换检验（seed 内臂标签置换）
random.seed(42)
obs = abs(med)
cnt = 0
for _ in range(10000):
    perm = []
    for s, d in deltas:
        # 翻转符号 = 交换臂标签
        perm.append(d if random.random() < 0.5 else -d)
    if abs(median(perm)) >= obs:
        cnt += 1
print(f"置换检验（10000 次符号置换）: p = {cnt/10000:.4f}")

# 轨迹（中位 g22_mean 按 tick）
print(f"\n=== g22_mean 轨迹（中位）===")
ticks = sorted({int(r["tick"]) for r in rows})
hdr = "tick   " + "".join(f"{t:>8}" for t in ticks)
print(hdr)
for arm in ("mem_on", "mem_off"):
    vals = []
    for t in ticks:
        v = [float(r["g22_mean"]) for r in rows if r["arm"] == arm and int(r["tick"]) == t]
        vals.append(median(v))
    print(f"{arm:<7}" + "".join(f"{v:>8.4f}" for v in vals))

# 明细
print(f"\n=== 逐 seed 明细 ===")
for s, d in deltas:
    on = term[(s, "mem_on")]; off = term[(s, "mem_off")]
    print(f"seed {s}: on={float(on['g22_mean']):.4f} off={float(off['g22_mean']):.4f} Δ={d:+.4f} | K_on={on['pop']} K_off={off['pop']}")
