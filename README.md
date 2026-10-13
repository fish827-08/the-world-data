# the-world-data

数字生命模拟项目的**实验数据仓库**（与主仓库 `the-world` 分离；实验数据 `.npz/.csv/.log` 等**不入主仓**）。

- 远端：`origin`（Gitee，权威）= `https://gitee.com/little-fishy/the-world-data`｜`github`（镜像，只保 main）= `fish827-08/the-world-data`
- 对账口径：主仓 `docs/实验记录.md` / `docs/实验台账.md` 中每条批次的「数据仓 `xxx/`」= 本仓对应目录

## 目录地图（2026-10-11 刷新）

### 可视化
| 路径 | 内容 | 量 |
|---|---|---|
| `viz/v0_sample/` | **可视化 v0 官方样例数据包**（60×120 · tick 300000→302000 · stride 20 · 101 帧 ×2 通道 resource/energy + 101 实体帧 + meta.json）——`viz/web` 前端直接加载 | 11M / 304 件 |
| `viz/v1_s2_sample/` | **可视化 v1 官方 s2 大世界样例**（480×960 · tick 4000→6000 · stride 20 · 101 帧 ×2 通道 resource/energy + 101 实体帧，源=旗舰60k快照 tick 4000）——`viz/README.md` 工作台默认加载 | 112M / 304 件 |

### 实验批数据（近 → 远）
| 路径 | 内容 | 量 |
|---|---|---|
| `bare_world/` | **纯斑块世界四臂批**（s2 · 2000t · seed 42；arm1 现状/arm2 置换 =两对照，arm3 地形/arm4 全规则 =两处理）+ 判读 `readout_s42.json` + `figs/` 3 图 | 45M / 16 件 |
| `energy_close_stepA/` | ENERGY-CLOSE 步A 五腿量级读数原始件（10-09，commit `6bbeadf`） | 40K |
| `e057_repw/` `e057_logs/` | E-057：rep_w 档扫 32 run（rpw0/05/20/50 × seed 207-214 × 2000t）数据 + log/status | 877K |
| `e056_m1/` `e056_logs/` | E-056：M1 正式批 8 run（seed 207-214 × 2000t）csv/summary + log/status | 205K |
| `m1_smoke/` | M1 冒烟批 | 208K |
| `k2_control_check/` | K=2 对照（bg_low=0.0，原崩溃 seed 全部稳定） | 12K |
| `smell4/` `smell_rd_01/` | 气味通道系列批 | 676K |
| `r323_20261002/` | R323 批（10-02） | 15M / 65 件 |
| `s2g2_newdev/` | s2 g2 新开发档 | 964K |
| `lto1/` | lto1 批 | 80K |
| `flagship60k/` | 旗舰档 60k | 380K |
| `hr200_4seed/` | HR200 4 seed | 680K |
| `s3_r257_v2/` `s35_r275/` `s35b_r283/` | S3 / S3.5 系列 | 356K |
| `batch_a/` `batch_a2/` `batch_b/` | 批次 A/A2/B（09-30） | 1.1M |
| `p1c/` `p1c_density/` `p1c_erase/` | P1-c 探针（距离/可达性门、密度、擦除） | 1.3M |
| `energy_fix_snap/` | 能量修复快照 | 4K |

### 工具产出 / 杂项
| 路径 | 内容 | 量 |
|---|---|---|
| `_rerun_logs/` | 历史重跑/复算日志与结果池 | 26M / 1319 件 |
| `experiments/` | 各实验脚本产出（csv/json；脚本在主仓） | 5.6M / 257 件 |
| `results/` | 扫描/分析产出（含 `s2_r243_s0/` = E-037 K=2 双稳态判据池） | 2.6M / 107 件 |
| `_clockcheck/` | 时基核对输出 | 253K |
| `_eval_reports/` | 评估报告数据 | 120K |

### 根级文件
| 文件 | 说明 |
|---|---|
| `run_note_E056.txt` | E-056 运行记录。🔴 被主仓 `docs/实验记录.md` 直引（@`a8d8f82`），**勿移动/改名** |
| `s2_r243_repl_newmachine.csv` | E-037 新机独立复现原始读数。🔴 被主仓 `docs/实验记录.md` 直引（@`53e65e2`），**勿移动/改名** |
| `energy_cap_s46.csv` | s46 能量帽扫描（历史批） |

## 纪律
- **本仓只存数据**——代码/文档/判读在主仓 `the-world`；根级被主仓直引的文件勿移动
- 单文件 **< 100 MB**（Gitee 硬限制）｜仓库总量 **< 1024 MB**（Gitee 免费配额）——接近时须归档/清理旧数据
- 新实验完成后由跑批人同步入库（避免游离散件）；批目录沿用实验编号命名
- 🔴 **不要指望 force-push 缩容**：Gitee 不回收旧对象（教训见下方时间线 2026-09-25）

## 时间线
- **2026-09-13 建立**：主仓因 `.npz` 快照在历史中反复提交累积 470MB（远端含未 GC 对象达 1048MB，超 Gitee 1024MB 配额无法推送）；主仓瘦身重建（~1.9MB），实验数据整体拆入本仓。
- **2026-09-25 两轮历史重写 + 删库重建**：
  - ① `git filter-repo` 抹掉 `_rerun_logs/cstep_snap_ext/{rolling,keypoints}/`（126MB 长跑中间检查点副本）；
  - ② 同日再抹掉 **218 个旧纪元 `.npz` 快照**（2026-09-24 之前，约 642MB）⇒ 工作树 774MB→32MB、`.git` 834MB→22MB（合计约 54MB）；
  - ⚠️ Gitee **不因 force-push 回收旧对象**（force 后仍报 913.656MB，反而叠加）⇒ 唯一干净解 = **删库同名重建**再推（实测新 clone 53MB，已 2026-09-25 完成）；
  - 🔴 **所有在此之前的 clone 全部失效**（含云端机器），须重新 `git clone`。依据：fish 09-25 批准；上板 R200/R201/R202/R203。
- **2026-10-11 本次整理**：① `viz/v0_sample/` 官方样例包入库；② README 重制为全仓结构总图；③ GitHub 镜像补齐至现行 HEAD。**未做任何数据搬迁**（避免主仓引用断链）。
- **2026-10-11 补**：`bare_world/` 纯斑块世界四臂批入库（ENV 场首批：地形→气候态水分→产能因子；无生物纯场 ⇒ 容量场静态；四臂 npz/csv/manifest + 判读产物 + 3 图）。
- **2026-10-13 补**：`viz/v1_s2_sample/` 大世界样例包入库（viz v1 合并 main 的配套件；`viz/README.md` 工作台默认加载路径）。

### 回滚镜像（两轮重写中被抹数据的唯一完整备份）
- 现位置：`the-world/_archive/桌面残留-20261003/_trash_purge_20260925/data_repo_mirror_backup.git`（824MB；本机保留，未入任何 git 仓）
- 旧 HEAD `d70c4ad`，含**全部**历史对象 ⇒ 两轮重写清掉的数据可从此镜像完整恢复。
- ⚠️ 勘误：旧版 README 所记路径 `Desktop\temp\_trash_purge_20260925\` 已随「桌面残留收纳批（10-03）」迁入上址，内容同一。
