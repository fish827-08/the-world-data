# the-world-data

数字生命模拟项目的**实验数据仓库**（与主仓库 `the-world` 分离）。

## 为什么要拆分
主仓库 `digital-life-sphere` 因 `.npz` 快照在历史中被反复提交，累积 **470 MB**，
加上远端未 GC 的对象达到 **1048 MB**，超过 Gitee 免费配额（1024 MB）导致**无法推送**。
2026-09-13 拆分：主仓库瘦身重建（~1.9 MB），实验数据移入本仓库。

## 内容
| 目录 | 内容 | 规模 |
|------|------|------|
| `data/snapshots/` | 模拟快照（.npz，单个 3–13 MB） | 22 文件 / 83.6 MB |
| `_rerun_logs/` | 实验日志与结果（.log/.csv/.json） | 139 文件 |
| `results/` | 扫描/分析产出 | 21 文件 |
| `_clockcheck/` | 时基核对输出 | 11 文件 |
| `_eval_reports/` | 评估报告数据 | 7 文件 |
| `experiments/` | 实验产出（csv/json；代码在主仓库） | 78 文件 |

## 纪律
- **本仓库只存数据**；代码与文档在 `the-world`
- 单文件 **< 100 MB**（Gitee 硬限制）
- 总容量 **< 1024 MB**（Gitee 免费配额）—— 接近时须归档/清理旧数据
- 新实验完成后，数据由 `[云端实验]` / `[本地开发]` 同步到此

## 时间线
- 2026-09-13：建立（主仓库容量超限拆分）
- 2026-09-25：**首次历史重写**（`git filter-repo`）—— 从全部提交中抹掉
  `_rerun_logs/cstep_snap_ext/{rolling,keypoints}/`（126 MB，长跑的中间检查点副本）。
  🔴 **所有在此之前的 clone 全部失效**，须重新 `git clone`（旧 clone 上 pull/merge 会冲突）。
  回滚镜像：`Desktop\temp\_trash_purge_20260925\data_repo_mirror_backup.git`（旧 HEAD `d70c4ad`）。
  依据：fish 2026-09-25 批准；上板 R200（删除预告）/ R201（force-push 预告）。
  ⚠️ 该批的**最终**快照 `oracle_m1.3_s46_ext.snapshot.npz` 保留。
