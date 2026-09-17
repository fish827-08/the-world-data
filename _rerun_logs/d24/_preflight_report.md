# Pre-Flight 检查报告

- 时间：2026-09-15 21:37:35
- 臂：['main', 'oracle'] / 种子：[42, 43, 44] / tick：3000

## C4 开关读回核对

| run | 结果 | 问题 |
|---|---|---|
| main_s42 | ✅ |  |
| main_s43 | ✅ |  |
| main_s44 | ✅ |  |
| oracle_s42 | ✅ |  |
| oracle_s43 | ✅ |  |
| oracle_s44 | ✅ |  |

## C5 规格自洽检查

> C4 问「开关有没有生效」；C5 问「生效的这些值彼此自洽吗」。

| run | 结果 | 问题 |
|---|---|---|
| main_s42 | ✅ |  |
| main_s43 | ✅ |  |
| main_s44 | ✅ |  |
| oracle_s42 | ❌ | **【保本语义不可达】** oracle 已启用，但 donation(0.05) < SIGNAL_COST(0.1) ⇒ return_ratio 结构性上限 = 0.5000 < 1.0 ⇒ 无论生态如何演化都不可能保本 （D-24 G-A 不过的根因；修复=反解 donation ≥ SIGNAL_COST/转化率） |
| oracle_s43 | ❌ | **【保本语义不可达】** oracle 已启用，但 donation(0.05) < SIGNAL_COST(0.1) ⇒ return_ratio 结构性上限 = 0.5000 < 1.0 ⇒ 无论生态如何演化都不可能保本 （D-24 G-A 不过的根因；修复=反解 donation ≥ SIGNAL_COST/转化率） |
| oracle_s44 | ❌ | **【保本语义不可达】** oracle 已启用，但 donation(0.05) < SIGNAL_COST(0.1) ⇒ return_ratio 结构性上限 = 0.5000 < 1.0 ⇒ 无论生态如何演化都不可能保本 （D-24 G-A 不过的根因；修复=反解 donation ≥ SIGNAL_COST/转化率） |

## C3 臂间轨迹差异

| seed | 臂对 | 结果 | 首个分歧 tick |
|---|---|---|---|
| 42 | main vs oracle | ✅ 有差异 | 1000 |
| 43 | main vs oracle | ✅ 有差异 | 1000 |
| 44 | main vs oracle | ✅ 有差异 | 1000 |

## R78-3 世界种子敏感性

| 臂 | 指标 | 各 seed 值 | std | 结果 |
|---|---|---|---|---|
| main | g15_final | [0.4916, 0.6861, 0.0443] | 0.2687 | ✅ |
| main | N_final | [3240.0, 3240.0, 497.0] | 1293 | ✅ |
| oracle | g15_final | [0.5128, 0.5973, 0.0137] | 0.2575 | ✅ |
| oracle | N_final | [389.0, 3239.0, 339.0] | 1355 | ✅ |

## 结论

❌ 未通过（3 项）⇒ **不得启动实验**

- C5 oracle_s42: ['**【保本语义不可达】** oracle 已启用，但 donation(0.05) < SIGNAL_COST(0.1) ⇒ return_ratio 结构性上限 = 0.5000 < 1.0 ⇒ 无论生态如何演化都不可能保本 （D-24 G-A 不过的根因；修复=反解 donation ≥ SIGNAL_COST/转化率）']
- C5 oracle_s43: ['**【保本语义不可达】** oracle 已启用，但 donation(0.05) < SIGNAL_COST(0.1) ⇒ return_ratio 结构性上限 = 0.5000 < 1.0 ⇒ 无论生态如何演化都不可能保本 （D-24 G-A 不过的根因；修复=反解 donation ≥ SIGNAL_COST/转化率）']
- C5 oracle_s44: ['**【保本语义不可达】** oracle 已启用，但 donation(0.05) < SIGNAL_COST(0.1) ⇒ return_ratio 结构性上限 = 0.5000 < 1.0 ⇒ 无论生态如何演化都不可能保本 （D-24 G-A 不过的根因；修复=反解 donation ≥ SIGNAL_COST/转化率）']
