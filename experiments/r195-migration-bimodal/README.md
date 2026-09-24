# R195 季节机制 · 迁徙实验（阴性） + 双峰证伪

**日期**：2026-09-24
**作者**：[云端·开发]
**分支**：`dev/terrain-s2` @ `042fd00`
**对应文档**：
- `the-world/docs/设计文档/实验报告-季节迁徙S4S5-无迁徙-20260924.md`
- `the-world/docs/设计文档/证伪-双峰在现行捕食公式下不可能-20260924.md`
- `the-world/docs/设计文档/建议-实现双峰的三条路径-20260924.md`

---

## 目录内容

| 文件 | 说明 |
|---|---|
| `mig_s{42,7,123,2024}.csv` | 迁徙探针原始输出（18000 tick，P=6000，`temp_sensitivity=6.0`；列：tick, N, centroid_lat, band_res, band_env, g16_mean） |
| `mig_s{42,7,123,2024}.summary.json` | 每个 seed 的完整判读摘要（含相位零分布检验内部量） |
| `band_move.csv` | S4 富集带移动探针（`temp_sensitivity=1`） |
| `band_move_ts6.csv` | S4 富集带移动探针（`temp_sensitivity=6`） |
| `migration_result_4seed.png` | 四 seed 判读图 |
| `migration_verdict_4seed.json` | 显著性结果（4 seed） |
| `bimodal-fitness/` | **双峰证伪子包**（见下） |

### `bimodal-fitness/`

| 文件 | 说明 |
|---|---|
| `bimodal_falsification_proof.txt` | 18 组参数全扫原始输出（126 行，全部"无内部谷"） |
| `analyze_bimodal_fitness.py` | 证伪脚本（与代码仓 `experiments/` 同名文件一致） |
| `README.md` | 证伪结论、公式行号、复现方式、诚实边界 |

---

## 结论一：R195 季节机制下**无迁徙**（阴性）

季节机制（赤纬 δ(t) = tilt·sin(2πt/P)）已正确实现，但迁徙实验 4 seed 一致阴性：

| seed | 零滞后 corr(质心, 光照带) | 相位零分布 p | 判定 |
|---|---|---|---|
| 42 | −0.022 | 0.964 | 无迁徙 |
| 7 | +0.010 | 0.984 | 无迁徙 |
| 123 | +0.053 | 0.852 | 无迁徙 |
| 2024 | −0.227 | 0.457 | 无迁徙 |

（原始数据 `migration_verdict_4seed.json`；4 seed p 全部 ≫ 0.05，零滞后 corr 全部接近 0
或为负 ⇒ **质心与光照带无任何相位关系**。）

**根因**（关键诊断）：

| 量 | 摆幅 | 含义 |
|---|---|---|
| `band_env`（光照带） | **35.8°** | 季节信号很强 ✅ |
| `band_res`（资源**存量**带） | **1.4–3°** | 食物几乎不动 ❌ |

> **季节移动的是"光"，不是"食物"。** 生物停在原地即可获得同等光照 ⇒ 驻留最优 ⇒ 无迁徙。

代码层根因：`ResourceField._regrowth_amount` 的再生速率**只耦合温度，完全不看光照**。

⇒ 这直接催生了 R196（光驱动再生）。见 `experiments/r196-light-regrowth/`。

---

## 结论二：双峰（进化分支）在现行捕食公式下**数学上不可能**

详见 `bimodal-fitness/README.md`。要点：

- 适应度地形 `W(g) = (1-g)^k·F + 1[g>gate]·[p(g)·σ(g)·E_prey·r − p(g)·c]`
- `p(g)`、`σ(g)` 对 `g` **单调不减**，`(1-g)^k` 单调不增 ⇒ 导数最多变号一次
- ⇒ **`g∈(0,1)` 上不存在内部极小（谷）**
- ⇒ 分裂选择（双峰）的必要条件不满足 ⇒ **不是"跑不出来"，是解空间里没有**

**18 组参数全扫**（`k` × 能量不对称 × 成本倍率 × 组合）**18/18 无内部谷**。

⚠️ 注意：`g=.3` 处 `W` 可能低于 `W(0)`（因 `(1-g)^k` 下降段），
这是**单向下降**而**不是谷** —— 判据要求"两侧都上升的局部极小"。原始输出中已标注"无内部谷"。

---

## 复现方式

```bash
export PYTHONPATH=/path/to/the-world   # 分支 dev/terrain-s2 @ 042fd00

# 迁徙探针（4 seed，3 周期）
for s in 42 7 123 2024; do
  python3.12 experiments/probe_migration.py --seed $s --ticks 18000 \
      --season-period 6000 --tilt-deg 23.44 --out mig_s$s.csv
done

# 判读
python3.12 experiments/analyze_migration.py mig_s*.csv

# 双峰证伪
python3.12 experiments/analyze_bimodal_fitness.py
```

---

## 诚实边界

1. 本包的迁徙实验是**阴性结论** —— 已如实记录，未做美化。
   阴性根因（食物带不动）已定位到具体代码行，并已由 R196 修复验证。
2. 双峰证伪是**解析结论**，不是动力学模拟结论。它证明该公式族的适应度地形无内部谷；
   不排除瞬态/非平衡的空间异质多峰。
3. 双峰证伪的参数扫描**未覆盖** `gain` / `floor` / `ceil` / `transfer_ratio` / `gate`。
   但结论依赖**单调性（结构性）**而非具体数值，故预期不变；彻底封口需补扫（见建议文档后续项）。
4. **未跑**动力学长程验证（如 200k tick 的 g16 分布直方图）。解析强于数值，
   但若质疑"解析没考虑种群结构"，补直方图实验是最直接的回应。

---

> 配套建议（如何真正造出双峰）见 `the-world/docs/设计文档/建议-实现双峰的三条路径-20260924.md`。
