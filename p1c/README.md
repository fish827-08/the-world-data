# p1c —— P1-c 距离/可达性门探针 · A4 产物（R355-A4｜R358-T3 入仓）

**探针**：`experiments/p1c_distance_probe.py` @ `538e13c`（分支 `dev/qingzhou-m0-instruments` @ `3872a2c`）
**最小测试**：`tests/test_p1c_distance_probe.py`（12 例；镜 D1 审计阻塞项解除，`3872a2c`）
**性质**：🔵 **纯测量探针——只出数，不预设结论**；P1-c 分支判读由天平据定稿 §5.1 条款执行，本目录只锁"产出"（读数与复跑证据）。

## 装置行（s2 预设；R320 纯零背景）

`rows=480 cols=960 patches=1700 pop=10000 rgm=1.195 bg_low=0.0/0.0`
`subpos=True（use_sim_core=False）`｜`k=2.5`｜`rd=False`｜`info=False`｜`alphabet=8`｜`max_count=30000`
（summary `readback` 逐字段回读自检，见各 `.summary.json`）

## 文件表

| 文件 | 说明 |
|---|---|
| `p1c_s207_t3000_v2.csv` + `.summary.json` + `run_s207_v2.log` | 🔵 **权威产物**：30 采样点（t=100..3000），探针 @ `538e13c`（含 pos_* 列） |
| `p1c_s207_t3000.csv` + `.summary.json` + `run_s207.log` | v1 存档（探针 @ `c52faa0`，无 pos_* 列）——provenance，勿当权威 |
| `smoke_s207_t60*.csv/.summary.json` | 60 tick 冒烟（v1/v2 各一） |
| `rerun_s207_t2000.csv` + `.summary.json` | 同日**独立重跑**（同 argv，仅 ticks 2000）——确定性证据 |
| `check_rerun_vs_csv.py` | 重跑 vs 权威 CSV 逐位核对脚本（纯读） |

## 结论摘要（观测值；判读另见板上裁定）

P1-c 判据核心读数 = **d>0 子集**（mem_bit 判据要求槽 ≠ 当前格；`pos_*` 列）：

| 池 | n | 中位 | p90 | d≤1 格(口径A) | 可直读(Moore,口径B) |
|---|---|---|---|---|---|
| 全槽（全池） | 876 290 | 0.723 | 1.385 | 81.1% | 92.0% |
| **d>0 子集** | 505 281 | 1.000 | 2.000 | 67.2% | **86.2%** |

- 口径A = 球面大圆距离 ≤1.0 格（单位 = 1 纬度格宽，定稿字面）
- 口径B = 引擎真值：记忆格 ∈ Moore 8 邻（含极点带特判）
- 全池 `d==0` 占 42.3%；`d≤1.5` 占 92.7%
- 🔴 判读口径（"86.2% ⇒ 都很近"一类结论）**不在本目录**：以板上裁定与 `docs/` 判读稿为准

## v1 / v2 关系（防混用）

- v1 = `c52faa0`（初版探针）｜v2 = `538e13c`（+pos_* 两口径子集列）← **权威**
- `[实测]` 两版**共享 13 列 × 30 采样点逐位一致**（除 `ms_per_tick_window`）⇒ 追加 pos_* 列未改任何既有测量值

## 独立重跑核对（镜 D1 要求⑤ / 确定性证据）

- `[实测]` `rerun_s207_t2000.csv` vs v2 前 20 采样点（t=100…2000）：**非时序列 0 差异**（20/20 行）
- 复跑核对（纯读，无需 numpy）：`python check_rerun_vs_csv.py`（exit 0 = 一致）

## 🔴 已知陷阱（引用本批数据前必读）

1. 🔴 **空池崩溃（已报板上待裁定）**：某采样点"全池零有效槽"时，探针在 pooled 打印处 rc=1
   （`None` 格式化 TypeError；此时 CSV/JSON 已写出）。本目录各产物**均非空池路径**，不受影响；
   T2 测试以 `--pop 1000` 绕避（详见 `tests/test_p1c_distance_probe.py` 头注）。
2. 🔴 `ms_per_tick_window` 为机负载敏感时序列 ⇒ **任何跨 run 逐位对比必须排除它**。
3. 🟡 别把全池读数当判据读数：mem_bit 判据相关的是 **d>0 子集**（`pos_*`），全池含 42.3% 同格槽。
4. 🟡 本批为 **480×960 大世界**；60×120 的几何常数（对角 ≈√2 格 / 跨缝 ≈1 格）见测试文件，勿跨装置外推。

## 复跑命令（cwd = 主仓/工作树根）

```bash
PYTHONIOENCODING=utf-8 python -m experiments.p1c_distance_probe \
  --device s2 --seed 207 --ticks 3000 --sample 100 --out <out>.csv
```

**证据标签**：`[实测]`（本仓 CSV/summary）｜`[文档]`（`docs/` 派工与判读稿）｜`[推断]`（本目录不含）
