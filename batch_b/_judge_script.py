# -*- coding: utf-8 -*-
"""批 B 判读（R282 预注册口径）：主门 = 捕食死亡份额配对差（rk_on−rk_off）<0 ≥14/24。"""
import csv
from statistics import median

def load(files):
    out = []
    for f in files:
        out.extend(csv.DictReader(open(f, encoding="utf-8")))
    return out

on = load(["_rerun_logs/batch_b/bb_sm_on_a.csv", "_rerun_logs/batch_b/bb_sm_on_b.csv"])
off = load(["_rerun_logs/batch_b/bb_sm_off_a.csv", "_rerun_logs/batch_b/bb_sm_off_b.csv"])

def term(rows):
    d = {}
    for r in rows:
        if r["tick"].strip() == "2000":
            d[int(r["seed"])] = r
    return d

ton, toff = term(on), term(off)
seeds = sorted(set(ton) & set(toff))
print(f"完整性: on {len(ton)} seed / off {len(toff)} seed / 配对 {len(seeds)}（预期 24）")

def share(r):
    starv = float(r["d_starv"]); old = float(r["d_old"]); pred = float(r["d_pred"])
    tot = starv + old + pred
    return pred / tot if tot > 0 else float("nan")

diffs = []
for s in seeds:
    a, b = share(ton[s]), share(toff[s])
    diffs.append((s, a - b, int(float(ton[s]["pop"])), int(float(toff[s]["pop"])),
                  float(ton[s].get("l1_visited_patch_frac", "nan")), float(toff[s].get("l1_visited_patch_frac", "nan"))))

neg = sum(1 for _, d, *_ in diffs if d < 0)
print(f"\n=== 主门 A：捕食死亡份额配对差（on−off）===")
print(f"负向（回避生效）: {neg}/{len(diffs)} | 通过线 ≥14/24 ⇒ {'✅ 通过' if neg>=14 else '❌ 不通过'}")
print(f"中位差: {median([d for _,d,*_ in diffs])*100:+.3f} pp")

dp = [po - pf for _, _, po, pf, *_ in diffs]
print(f"\n=== 支持 B：pop 配对 on−off ===")
print(f"on>off: {sum(1 for d in dp if d>0)}/24 | 中位 {median(dp):+.0f}")

dl = [lo - lf for *_, lo, lf in diffs]
print(f"\n=== 支持 C：l1 配对 on−off ===")
print(f"on>off: {sum(1 for d in dl if d>0)}/24 | 中位 {median(dl)*100:+.3f} pp")

print(f"\n{'seed':>5} {'Δshare(pp)':>11} {'K_on':>6} {'K_off':>6} {'share_on':>9} {'share_off':>9}")
for s, d, po, pf, lo, lf in diffs:
    print(f"{s:>5} {d*100:>+10.3f} {po:>6} {pf:>6} {share(ton[s])*100:>8.2f}% {share(toff[s])*100:>8.2f}%")
