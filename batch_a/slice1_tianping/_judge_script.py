# -*- coding: utf-8 -*-
"""批 A 判读（R275 预注册口径）：主门 = l1_visited_patch_frac 配对差（sm_on−sm_off）>0 计数。
用法：python _batchA_judge.py [分片2目录] [片1目录(可选)]"""
import csv, sys
from statistics import median

TARGET = "l1_visited_patch_frac"

def load(path):
    return list(csv.DictReader(open(path, encoding="utf-8")))

def term(rows, seed, tick="2000"):
    for r in rows:
        if int(r["seed"]) == seed and r["tick"].strip() == tick:
            return r
    return None

def judge(slices, label):
    """slices = list of (on_files, off_files)；合并所有分片"""
    on, off = {}, {}
    for on_files, off_files in slices:
        for f in on_files:
            for r in load(f):
                if r["tick"].strip() == "2000":
                    on[int(r["seed"])] = r
        for f in off_files:
            for r in load(f):
                if r["tick"].strip() == "2000":
                    off[int(r["seed"])] = r
    seeds = sorted(set(on) & set(off))
    diffs = []
    for s in seeds:
        a = float(on[s][TARGET]); b = float(off[s][TARGET])
        diffs.append((s, a - b, float(on[s]["pop"]), float(off[s]["pop"]),
                      float(on[s].get("bg_resid_frac", "nan")), float(off[s].get("bg_resid_frac", "nan"))))
    pos = sum(1 for _, d, *_ in diffs if d > 0)
    print(f"\n===== {label}：{len(seeds)} seed =====")
    print(f"主门 Δl1>0: {pos}/{len(seeds)} | 中位差 {median([d for _,d,*_ in diffs])*100:+.3f} pp | 均值 {sum(d for _,d,*_ in diffs)/len(diffs)*100:+.3f} pp")
    dp = [po - pf for _, _, po, pf, *_ in diffs]
    print(f"pop 配对 on>off: {sum(1 for d in dp if d>0)}/{len(dp)} | 中位 {median(dp):+.0f}")
    print(f"{'seed':>5} {'Δl1(pp)':>9} {'K_on':>6} {'K_off':>6}")
    for s, d, po, pf, *_ in diffs:
        print(f"{s:>5} {d*100:>+8.3f} {po:>6.0f} {pf:>6.0f}")
    return diffs

if __name__ == "__main__":
    d2 = "the-world-data/batch_a/slice2_yunqui"
    slices2 = [([f"{d2}/ba_sm_on_s1.csv", f"{d2}/ba_sm_on_s2.csv"],
                [f"{d2}/ba_sm_off_s1.csv", f"{d2}/ba_sm_off_s2.csv"])]
    judge(slices2, "片2（云归 137-148）")
    if len(sys.argv) > 1:
        d1 = sys.argv[1]
        slices1 = [([f"{d1}/batch_a_sm_on.csv"], [f"{d1}/batch_a_sm_off.csv"])]
        judge(slices1 + slices2, "全批（片1+片2 合并）")
