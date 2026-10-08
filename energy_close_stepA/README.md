# energy_close_stepA —— ENERGY-CLOSE 步A · 5 腿量级读数原始件

> 落件人 澜舟 `[开发·二线]`｜2026-10-09｜代码基线 `task/ENERGY-CLOSE @ 2111d15`（干净树）
> 上板口径：板帖 `the-world` 主仓 `_share/讨论板.md`，读数首报 commit `7ddafa0`。
> PI 10-08 23:4x 班催办②「读数原始件未落盘即未生效」⇒ 本目录即该原始件的归档位。

## 文件

| 文件 | 内容 |
|---|---|
| `leg_readout_20261009.json` | 3 run（seed 7/8/9）× 1500 tick 的逐通道 sidecar（30 行/run，`row_every=50`）+ totals + A/B 对拍 + 与板 `@7ddafa0` 对账结果 + provenance + 档偏差登记 |

生成器（**在主仓，不在本数据仓**）：`the-world` 主仓 `experiments/stepa_leg_readout.py`
（commit `93342ed`，R342 编排脚本入库）。复现命令：

```bash
# 于 .worktrees/ENERGY-CLOSE 内，须干净树（provenance.git_dirty 必须为 false）
PYTHONUTF8=1 ../../.venv/Scripts/python.exe experiments/stepa_leg_readout.py \
    --out <数据仓>/energy_close_stepA/leg_readout_20261009.json
```

## 档（caliber）

60×120（7,200 格，**仓库默认微型档**，非 480×960 正式档）｜初始种群 **200**｜斑块 30｜
`resource_dynamics` 关｜`corpse_enabled` 关｜`predation.enabled` 开（默认）｜`use_sim_core=False`｜
`energy_probe.enabled=True row_every=50`。seed 7/8/9 × 1500 tick。

🔴 **与 10-07 v0 装置表的唯一偏差 = 初始种群**：出数批实测跑的是仓库默认 **200**，不是 v0 表的
400。判据 = seed7 关/开 `digest (670522, 88366.190893)` + `rng_draws 23269` **只在 pop=200 复现**
（pop=400 实测 `(1239687, 150697.441427)` / `30820`）。⇒ 板帖「协议照 v0」这句在初始种群项不成立，
已在 JSON 的 `caliber.deviation_note` 原文登记。**比例类结论同档自洽不受影响；绝对量级禁与 10-07 v0 互比。**

## 读数（1500 tick 累计流量，单位=能量，非净额）

| seed | dis_meta | dis_move | dis_attack | dis_signal | esc_death_e |
|---|---|---|---|---|---|
| 7 | 248848.38 | 21330.90 | 67.70 | 10801.30 | 29869.18 |
| 8 | 221445.17 | 20152.05 | 64.70 | 9196.00 | 35528.15 |
| 9 | 297313.91 | 17794.96 | 57.70 | 11396.80 | 25892.72 |

`esc_pred_e` / `esc_pred_s` = **`null`**（未埋点 ⇒ 未观测 ≠ 0，砚⑥）⇒ 上表是 **5/7 腿下界**。

## 门与自检（全过，JSON 内有据）

- A/B：seed7 探针关 vs 开 ⇒ `bit_equal=true` + `rng_equal=true`（探针只读，零行为/零 RNG）。
- 与板 `@7ddafa0` 逐位对账：digest / rng_draws / 5 腿累计 × 3 run 全中，`mismatches=[]`。
- 自检①早停不静默（`ticks_run == 1500` ×3）｜②`rows_emitted=30 > 0` 且与 totals 行数一致｜
  ③`env.sim_core_usable=true`（本机**有**可用编译扩展，读数走 Python 路径是**档选择**，不是"无扩展"）｜
  ④对账不齐 ⇒ 禁入库。
- provenance：`git_commit=2111d15…`、`git_dirty=false`、`code_tree_sha256`、`config_fingerprint` 全在。

## 用途边界（PI 裁原样）

只出**量级 / 点火阻塞判据**，不是"能量偏差全账闭合"，也不是 S0 结论发布证据；
S0 复算不复用本探针链路（R394）⇒ 复算脚本届时另立。判读口径归砚。
