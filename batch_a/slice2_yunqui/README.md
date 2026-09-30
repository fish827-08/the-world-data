# 批 A · 分片 2（云归沙盒）

**R276 派工执行 · seeds 137–148（12 seed）× sm_on/sm_off × 2000t**

## 装置口径（批 A 预注册 §二 = S2 同款）

| 项 | 值 |
|---|---|
| 世界 | `rows=480 cols=960 patches=1700 pop=10000` |
| 时长/采样 | `ticks=2000 sample=250`（每 run 8 采样点） |
| 资源 | `rgm=1.195 bg_low_prod_frac=0.4 bg_low_cap_mult=0.05`，rd 开 |
| 臂 | `--arms on`（rd 全开，唯一变量 = smell） |
| **sm_on** | `--smell-channels food,prey --use-in-move` |
| **sm_off** | 默认全关（= 回滚点） |
| 冻结树 | `29c94e1`（`git archive`，含 R275 T1 探针改造） |
| 机器 | 云归沙盒（32 vCPU / 126GB RAM），4 进程 |

## 文件

| 文件 | 说明 |
|---|---|
| `ba_sm_on_s1.csv` | sm_on，seeds 137–142 |
| `ba_sm_on_s2.csv` | sm_on，seeds 143–148 |
| `ba_sm_off_s1.csv` | sm_off，seeds 137–142 |
| `ba_sm_off_s2.csv` | sm_off，seeds 143–148 |
| `*.log` | 各进程完整 stdout/stderr（含装置行首行） |
| `*.summary.json` | 探针自产 summary |
| `ba_slice2_verdict.json` | 机器可读判读（配对差逐 seed 明细 + 三支柱汇总） |
| `run_batch_a2.sh` | 起跑脚本（装置口径显式锁死） |
| `_DEPLOY_MANIFEST.txt` | 部署清单（deployed_by=yungui） |

## 完整性

- 12 seed × 2 臂 = 24 run，**每 run 末 tick = 2000**（无早停/灭绝截断）；
- 每 seed 8 采样点（250…2000）。

| CSV | md5 |
|---|---|
| `ba_sm_on_s1.csv` | `36f3ce15bbedb07dfd4a2eb6d0cb67be` |
| `ba_sm_on_s2.csv` | `b74fd952705cae8beb1e4147b6cb3a4c` |
| `ba_sm_off_s1.csv` | `bb5924b8274c0e0138a19e948a6d3ec1` |
| `ba_sm_off_s2.csv` | `d66784ac45241443bfcdc3bd06dfd543` |

## 判读摘要（分片独立口径；终判 = 全批 24 seed 合并）

| 支柱 | 量 | 结果 |
|---|---|---|
| **A（主门）** | `l1_visited_patch_frac` 配对差 @t=2000 | **12/12 为正**，中位 **+0.0083**，均值 +0.0093 |
| **B** | `bg_resid_frac` 配对差 | 12/12 **下降**（中位 −0.0026）⇒ 气味驱动个体离开背景 |
| **B** | `l2_visited_frac` 配对差 | 12/12 上升（中位 +0.0083） |
| **C** | `pop` 配对差 | **12/12 为正**，中位 **+464**（+8%），均值 +447 |

性能（本沙盒）：`ms_per_tick` 中位 sm_off 44.76 ｜ sm_on 46.36 ⇒ smell 净开销 **+4.43 ms/tick（+9.9%）**。

## ⚠️ 已知事故与纠错（诚实登记）

本目录数据为**修正版**。首次起跑（12:32）因 R276 派工命令模板漏 `--patches/--pop`
⇒ 静默退回 S1 默认装置（`patches=480 pop=2000`）；12:37 装置行自查发现 ⇒ 停机、
清产物、补全口径后 **12:40 重跑**。本目录所有数据均来自修正版（装置行已逐进程核对）。
详见讨论板 R278（双坑同源复盘）。
