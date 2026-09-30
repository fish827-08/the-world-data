# -*- coding: utf-8 -*-
"""S3.5b 四进程编排器（R283）：按代梯度补测，seeds 165-172。"""
import os
import subprocess
import sys

ROOT = r"C:/Users/圣羽/Desktop/temp/tempCode/the-world"
os.chdir(ROOT)
PY = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
os.makedirs("_rerun_logs/s35b", exist_ok=True)

jobs = [("165,166", "a"), ("167,168", "b"), ("169,170", "c"), ("171,172", "d")]
procs = []
for seeds, tag in jobs:
    logf = open(f"_rerun_logs/s35b/s35b_{tag}.log", "w", encoding="utf-8")
    p = subprocess.Popen(
        [PY, "-u", "-m", "experiments.s3_memory_probe",
         "--seeds", seeds, "--weight-gene",
         "--out", f"_rerun_logs/s35b/s35b_{tag}.csv"],
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
print(f"[all] S3.5b 完成 rc={rc}", flush=True)
sys.exit(rc)
