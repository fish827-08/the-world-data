"""p1c 确定性核对：独立重跑 vs 权威 CSV（镜 D1 审计要求⑤）。

口径：`rerun_s207_t2000.csv` 与 `p1c_s207_t3000_v2.csv` 的 t=100..2000 段
（20 采样点）逐字段比对，**排除 `ms_per_tick_window`**（机负载敏感时序列）。

用法（纯读，标准库即可，无需 numpy）：
    python check_rerun_vs_csv.py
    exit 0 = 逐位一致；exit 1 = 存在差异（明细打印）
"""
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXCLUDE = {"ms_per_tick_window"}
A = "rerun_s207_t2000.csv"
B = "p1c_s207_t3000_v2.csv"
TICKS = 2000


def load(name):
    with open(HERE / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    a = load(A)
    b = [r for r in load(B) if int(r["tick"]) <= TICKS]
    if [r["tick"] for r in a] != [r["tick"] for r in b]:
        print("🔴 tick 网格不一致，无法比对")
        return 1
    diffs = [(ra["tick"], k, ra[k], rb[k])
             for ra, rb in zip(a, b) for k in ra
             if k not in EXCLUDE and ra[k] != rb[k]]
    tdiff = sum(1 for ra, rb in zip(a, b)
                if ra["ms_per_tick_window"] != rb["ms_per_tick_window"])
    print(f"行数={len(a)}  非时序列差异={len(diffs)}  "
          f"ms_per_tick_window 不同行={tdiff}/{len(a)}（预期不同）")
    for d in diffs[:20]:
        print("  ", d)
    ok = not diffs
    print("结论:", "✅ 逐位一致（除时序列）" if ok else "🔴 存在差异")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
