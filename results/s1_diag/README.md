# `results/s1_diag/` —— S1 诊断批（R217 §三 派工 A / `[本地开发]` 老工，2026-09-27）

> **一句话**：回答 **"K=3 000 被什么限制"** —— 扫 `patch_regrowth_mult`（斑块再生倍率）4 档 × 3 seed，看 K / 饱和度 / 死因怎么响应。

## 一、产物

| 文件 | 内容 |
|---|---|
| `rgm<档>_s<seed>.csv` | 逐采样（每 250 tick）轨迹：`pop`、`saturation`、`ms_per_tick`、`mean_energy`、`mean_gen`、**死因累计三列**（`d_starv`/`d_old`/`d_pred`） |
| `rgm<档>_s<seed>.summary.json` | 单 run 汇总（`switches` / `result` / `runs`）；`result.death_cause_tail` = **平台期（末 20% 采样窗口增量）**死因占比 |
| `rgm<档>_s<seed>.log` | 运行日志（含进度条与 ms/tick 轨迹）——**注意**：`rgm0.6_s42.log` / `rgm0.4_s43.log` 被第二个驱动器实例以 argparse 用法文本**覆盖**（见 §四-3），CSV/summary 未受影响 |
| `s1_scan_table.json` | 驱动器末段自动汇总表 |
| `_transient_earlystop/` | **作废档**：早停瞬态产物（首轮 3 个 + 次轮 4 个）⇒ **K 不可用**，只留档（原因见 §三） |
| `_driver.log` | `--skip-existing --retries 1` 那轮的驱动器输出 |

## 二、配置（与 T4 逐字段一致）

```
480×960（460 800 格）｜patches 480｜pop 2000｜ticks 40000｜sample 250
subpos on｜speed_max 0.125 / gain 0.125 / subdiv 80（R = v_max×subdiv = 10）
k 2.5｜max_count 30000｜bg_production_zero = True｜patch_regrowth_mult ∈ {1.195, 0.8, 0.6, 0.4}
seeds 42 / 43 / 44  ⇒ 共 12 run（6 路并发 × 2 轮）
```

## 三、🔴 有效性判定（12/12 全长，无截断）

判据（R217 钉死）：**K 必须取全长 40 000 tick 末端**；`final_tick = 40000` 且 `stop = "tick 用尽"` 才算有效。

- **有效 12 / 无效 0**（`_transient_earlystop/` 里 7 个 summary 均为**早停瞬态**：终止原因"平台期（连续 4 段 <3%）"，实测 tick 4 500–26 000，而同期全长档仍在爬升 ⇒ 按 R150/R194 教训㉒ 作废）。
- ⚠️ 本批的早停是**两次驱动器实例并发**造成的混跑：一实例用 `--stop-stable 4`（默认），另一实例用 `--stop-stable 0`。盘上文件曾混着两者 ⇒ **中间态读数不可引用**；本目录是**全部收工后的 12/12 全长**版本。

## 四、三条必读事实

1. **同档可复现**：`rgm=1.195`（= T4 档）在本批给 **K = 969/901/915**，且用 **T4 当时的提交 `d92cf84`** 重跑 1 000 tick 的轨迹与本批**逐点一致**（t=250/500/1000/2000 → 51/84/206/516）⇒ **本批可归因**。
2. 🔴 **T4 的 K = 3 003.5 复现不出来**：同配置重跑差 **3.28×**。已排除代码漂移 / `rgm∈{1.195,3.0}` / `bg_production_zero∈{True,False}` / `sim_core.so`(三棵树都没有) / 13.5 能量 preset（300/600、eat_eff 7.5、assim .4）——**四臂 + 三能量臂没有任何一臂落在 T4 轨迹附近**（t=1000：T4 = 628 vs 我们的臂 = 161–261 或 19 035）⇒ **T4 那批缺 provenance**（`steady_k_probe.py` 的 summary **不记** `git_commit` / `config_fingerprint` / `pop` / `rgm` / `bgzero`）⇒ **T4 的 K 不可作为定量锚点**。
3. **K ∝ 再生倍率近似线性**（4 档最小二乘幂 **0.95**；seed 均值口径 0.96）⇒ `K ≈ 744 × rgm^0.95`（rgm=1 时 744）⇒ 反推：K=1 944 ⇒ rgm≈2.0；K=1 000 ⇒ rgm≈1.12。
   饱和度**全程 0.94–0.96 不随 rgm 变化** ⇒ **"饱和度"是失灵的稀缺指标**（见板 R224 §二-2）。

## 五、provenance

| 项 | 值 |
|---|---|
| 代码树 | 冻结树 = 主仓 `1fcbe0a`（含 S1 探针改动 `816ca6f`：死因 3 列 + `--patch-regrowth-mult` + 驱动器） |
| 提取方式 | `git archive 1fcbe0a \| tar -x -C C:\Users\圣羽\Desktop\temp\_s1_frozen`（F-R9：他人有未提交改动时不动主树） |
| 解释器 | 本仓 `.venv/Scripts/python.exe`（冻结树无 `.venv`） |
| 产物对应 | **本目录 = 全部 12 run 走完 40 000 tick 后的最终版本**；中间态已挪入 `_transient_earlystop/` |
