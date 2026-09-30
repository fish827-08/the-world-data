# -*- coding: utf-8 -*-
"""S3.5 四进程编排器（R276）：spawn 4 分片并等待全部完成。"""
import os
import subprocess
import sys

ROOT = r"C:\Users\圣羽\Desktop\temp\tempCode\the-world"
os.chdir(ROOT)
PY = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
os.makedirs("_rerun_logs/s35", exist_ok=True)

jobs = [
    ("149,150,151,152", "a"),
    ("153,154,155,156", "b"),
    ("157,158,159,160", "c"),
    ("161,162,163,164", "d"),
]
procs = []
for seeds, tag in jobs:
    logf = open(f"_rerun_logs/s35/s35_{tag}.log", "w", encoding="utf-8")
    p = subprocess.Popen(
        [PY, "-u", "-m", "experiments.s3_memory_probe",
         "--seeds", seeds, "--weight-gene",
         "--out", f"_rerun_logs/s35/s35_{tag}.csv"],
        stdout=logf, stderr=subprocess.STDOUT,
    )
    procs.append((tag, p, logf))
    print(f"[spawn] {tag} seeds={seeds} pid={p.pid}", flush=True)

rc = 0
for tag, p, logf in procs:
    r = p.wait()
    logf.close()
    print(f"[done] {tag} rc={r}", flush=True)
    rc |= r
print(f"[all] S3.5 完成 rc={rc}", flush=True)
sys.exit(rc)
