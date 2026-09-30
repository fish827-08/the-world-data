# -*- coding: utf-8 -*-
"""批 B 四进程编排器（R282）：risk+kin 通道，seeds 125-148，4 片。"""
import os
import subprocess
import sys

ROOT = r"C:/Users/圣羽/Desktop/temp/tempCode/the-world"
os.chdir(ROOT)
PY = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
os.makedirs("_rerun_logs/batch_b", exist_ok=True)

# 装置 = 批 A 同款（逐字段核对：patches 1700 / pop 10000 / bg_low 0.4+0.05 / arms on）
BASE = ["--ticks", "2000", "--sample", "250", "--arms", "on",
        "--patches", "1700", "--pop", "10000",
        "--bg-low-prod-frac", "0.4", "--bg-low-cap-mult", "0.05"]
jobs = [
    ("125,126,127,128,129,130,131,132,133,134,135,136", "on_a",  ["--smell-channels", "risk,kin", "--use-in-move"]),
    ("125,126,127,128,129,130,131,132,133,134,135,136", "off_a", []),
    ("137,138,139,140,141,142,143,144,145,146,147,148", "on_b",  ["--smell-channels", "risk,kin", "--use-in-move"]),
    ("137,138,139,140,141,142,143,144,145,146,147,148", "off_b", []),
]
procs = []
for seeds, tag, extra in jobs:
    logf = open(f"_rerun_logs/batch_b/bb_sm_{tag}.log", "w", encoding="utf-8")
    p = subprocess.Popen(
        [PY, "-u", "-m", "experiments.s2_depletion_probe",
         "--seeds", seeds] + BASE + extra +
        ["--out", f"_rerun_logs/batch_b/bb_sm_{tag}.csv"],
        stdout=logf, stderr=subprocess.STDOUT,
    )
    procs.append((tag, p, logf))
    print(f"[spawn] {tag} pid={p.pid}", flush=True)

rc = 0
for tag, p, logf in procs:
    r = p.wait()
    logf.close()
    print(f"[done] {tag} rc={r}", flush=True)
    rc |= r
print(f"[all] 批 B 完成 rc={rc}", flush=True)
sys.exit(rc)
