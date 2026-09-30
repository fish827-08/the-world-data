#!/bin/bash
# 批 A 分片 2 起跑脚本（R276 派工；云归）—— 4 进程
# 🔴 装置口径（批 A 预注册 §二）= S2 同款：480x960 / patches=1700 / pop=10000 /
#    bg_low 0.4+0.05 / rd on / 2000t；唯一变量 = smell。
#    ⚠️ 派工令命令模板漏了 --patches/--pop（会静默退回 S1 默认 480/2000）⇒ 此处显式补全。
cd /root/world/batch_a2 || exit 1
COMMON="--rows 480 --cols 960 --patches 1700 --pop 10000 --ticks 2000 --sample 250 \
--rgm 1.195 --arms on --bg-low-prod-frac 0.4 --bg-low-cap-mult 0.05"
SMELL="--smell-channels food,prey --use-in-move"

python3 -u -m experiments.s2_depletion_probe --seeds 137,138,139,140,141,142 $COMMON $SMELL \
  --out results/ba_sm_on_s1.csv  > results/ba_sm_on_s1.log  2>&1 &
python3 -u -m experiments.s2_depletion_probe --seeds 143,144,145,146,147,148 $COMMON $SMELL \
  --out results/ba_sm_on_s2.csv  > results/ba_sm_on_s2.log  2>&1 &
python3 -u -m experiments.s2_depletion_probe --seeds 137,138,139,140,141,142 $COMMON \
  --out results/ba_sm_off_s1.csv > results/ba_sm_off_s1.log 2>&1 &
python3 -u -m experiments.s2_depletion_probe --seeds 143,144,145,146,147,148 $COMMON \
  --out results/ba_sm_off_s2.csv > results/ba_sm_off_s2.log 2>&1 &
wait
echo "ALL_DONE $(date '+%F %T')" > results/_ALL_DONE
