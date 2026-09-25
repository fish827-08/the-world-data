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
- 2026-09-25：**第二轮历史重写**（同日合并进行）—— 再从全部提交中抹掉
  **218 个旧纪元 `.npz` 快照**（13.5 之前 = 2026-09-24 之前，约 642 MB）。
  结果：工作树 774MB → **32MB**；`.git` 834MB → **22MB**；合计约 **54MB**。
  🔴 **远端必须删库重建**：Gitee **不会**因 force-push 回收旧对象（force-push 后仍报
  935MB，随后 913.656MB）⇒ 只有删掉远端仓库再**同名重建**，推上去才是干净的 54MB。
  ⇒ 重建步骤见本节末「远端重建」。
  🟢 **回滚镜像**：`Desktop\temp\_trash_purge_20260925\data_repo_mirror_backup.git`
  （824MB，旧 HEAD `d70c4ad`，含**全部**历史对象）⇒ 被清数据**可完整恢复**。

## 远端重建（Gitee，需 owner 在网页操作）

1. 打开 `https://gitee.com/little-fishy/the-world-data` → **管理** → **删除仓库**
   （按页面要求输入仓库名确认）。
2. **同名重建**：新建仓库，路径仍填 `the-world-data`，**不要**勾选初始化 README/.gitignore
   （保持空仓）⇒ URL 不变。
3. 回到本机执行：
   ```
   cd the-world/the-world-data
   git -c credential.helper=manager push -u origin main
   ```
   ⇒ 推上去即为干净的 54MB。
4. 🔴 **所有旧 clone 全部失效**，须重新 `git clone`（含云端机器）。
