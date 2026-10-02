# s2g2_newdev —— S2 判据② 新装置档批（12 run × 40 000 tick）

**批次**：R329 短路径第1 步｜天平 15:27 起跑，6 路并行，ALLDONE 248.7 min，失败 0
**冻结树**：`git archive` @ `4059f24`（含 R331 甲案`from_field` 直读 bg_production_zero）
**产物目录**：本机 `_rerun_logs/s2g2_newdev/`（含快照，未入库）；本仓 `results/` 为CSV + summary

## 装置行（唯一变量 = rd）

`rows=480 cols=960 patches=1700 pop=10000 rgm=1.195 ticks=40000 sample=250`
`bg_low_prod_frac=0.0 bg_low_cap_mult=0.0`｜`--sparse-fields` 开（A1 稀疏化，R331 §二）

| 臂 | 含义 |
|---|---|
| `off` | rd 关（`resource_dynamics` 关） |
| `on` | rd 开（rest 休耕 / dead 杀 / demoted 降级） |

- **种子**：201–206（6 个世界，**全部 A 支**——`bg_low_frac_actual=0.0`，12/12）
- 🔴 **本批是首次干净的单变量 rd 对照**：旧批的A/B 支抽奖已在 R326 撤除、R331 甲案根除

## 完整性（天平 22:30 独立复核）

| 项 | 要求 | 实测 |
|---|---|---|
| run 数 | 6 seed × 2 臂 | **12/12** |
| 每 run 行数 | 160 采样点 | **160**（+表头=161） |
| 末 tick | 40000 | **12/12 = 40000** |
| `bg_low_frac_actual` | 0.0 | **12/12 = 0.0** |
| 编解码失败 | 0 | **0**，rc 全 0 |

## 结论（详见 `docs/R336-判据②批判读-20261002.md`）

| 判据 | 实测 | 判定 |
|---|---|---|
| **主判据 `patch_sat_init_var`（on > off）** | **0/6**（Δ −0.011 ~ −0.022） | ❌ **不成立** |
| S1 `l1_visited_patch_frac`（on > off） | 0/6（Δ −0.011 ~ −0.045） | ❌ 反向 |
| S2 `patch_sat_mean`（on < off） | 0/6（Δ **+0.031 ~ +0.061**） | ❌ 反向（斑块更饱和） |
| S3 止损红线（K 降幅 ≤50%） | **K 比中位 0.438** | 🔴 **6/6 击穿** |

⇒ **判据② 不成立** ⇒ **C3 硬前置判死** ⇒ 路线改写见 R337（气味+记忆 → C3）。

## 🔴 已知陷阱（引用本批数据前必读）

1. 🔴 **`criterion_2` 字段在分片运行下恒为 `null`**（代码缺陷，`s2_depletion_probe.py:604-636`
   要求同seed 双臂同批，单 run summary 配不上对）⇒ **不要只看 summary 的 verdict**；
   本仓数据请用 `_judge_s2g2.py` 或 `docs/R336` 稿的独立重算。
2. 🔴 **旗舰 60k 是"记忆臂"on/off，不是 rd 臂**（臂名 `mem_off`/`mem_on`）⇒ 跨批对照时勿混变量。
3. 🔴 **旗舰 8 seed = A 支 5 + B 支 3**（B：167/170/172）⇒ 幅度类读数须按支分层。

## 复跑

- 判读：`experiments/_judge_s2g2.py`（天平 22:20 产物）
- 跨批复核：`experiments/_verify_r336_table.py` → `_verify_r336_table.json`（已存本目录）
- 交叉验证：`experiments/_crosscheck_r336_vs_60k.py`（内评）

**证据标签**：`[实测]`（本仓 CSV/summary）｜`[文档]`（R336 判读稿）｜`[推断]`（机制解读）