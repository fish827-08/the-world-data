#!/bin/bash
# 旗舰 60k · off 臂 8 seed（R288 执行序 §二-1；云归）
# 装置：S3 同款 rows=480 cols=960 patches=1700 pop=10000 ticks=60000 sample=2000 --arms off
# seed 165 已由 _alive_test 转正式（硬链接 fl_s165_off.csv，独立进程，不在此脚本内）
# 本脚本起 3 进程覆盖 166-172（共 7 run），与 165 进程合计 4 进程 —— 均衡：
#   P165(外部): [165]         ← 已在跑
#   g1: [166,167,168]         ← 3 run
#   g2: [169,170]             ← 2 run
#   g3: [171,172]             ← 2 run
# ⚠️ 若不均衡（如 2/2/3），尾段会因"最短队列先空"造成核闲置。
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
cd /root/world/flagship60k || exit 1
CO="--ticks 60000 --sample 2000 --arms off"

python3 -u -m experiments.s3_memory_probe --seeds 166,167,168 $CO --out results/fl_g1.csv > results/fl_g1.log 2>&1 &
python3 -u -m experiments.s3_memory_probe --seeds 169,170     $CO --out results/fl_g2.csv > results/fl_g2.log 2>&1 &
python3 -u -m experiments.s3_memory_probe --seeds 171,172     $CO --out results/fl_g3.csv > results/fl_g3.log 2>&1 &
wait
echo "OFF_SLICE_DONE $(date '+%F %T')" > results/_OFF_DONE
