# Chapter 3: 单变量图形的绘制

## Core Idea
单变量图用于理解一个连续变量的分布形态。不要只画一种图：直方图看频数结构，密度图看平滑形态，Q-Q/P-P 图检查理论分布，ECDF 展示不依赖分箱的累积比例。

## Frameworks Introduced
- **分布诊断四件套**：Histogram → KDE → Q-Q/P-P → ECDF。
  - When to use: 数据探索、建模前检查、异常值与分布假设诊断。
  - How: 先看原始频数，再看平滑结构，然后检验理论分布，最后用 ECDF 比较百分位和尾部。
- **参数敏感性检查**：直方图的 bins 与 KDE 的 bandwidth 都会改变视觉结论。
  - How: 至少比较两组合理参数；若结论随参数剧烈变化，应回到样本量与原始数据。
- **经验与理论对照**：用 Q-Q/P-P 或 ECDF 与 CDF 对比，而不是根据直方图外观声称“服从正态分布”。

## Key Concepts
- **直方图**：将连续值分箱后显示每个区间的频数或密度。
- **核密度估计 KDE**：用核函数叠加得到平滑密度估计。
- **带宽 bandwidth**：控制 KDE 平滑程度；过小产生伪峰，过大掩盖结构。
- **Q-Q 图**：比较样本分位数与理论分位数，对尾部偏差敏感。
- **P-P 图**：比较经验累计概率与理论累计概率，更强调分布主体。
- **ECDF**：每个观测值对应不大于该值的样本比例，不需要分箱或带宽。
- **CDF**：给定理论分布的累积分布函数，可与 ECDF 直接比较。

## Mental Models
- **Use raw counts before smooth curves**：先确认样本量和频数，再相信 KDE 的形状。
- **Use Q-Q for tails, P-P for center**：检验极端值和尾部优先 Q-Q，观察主体拟合优先 P-P。
- **Think in percentiles with ECDF**：当问题是“多少样本低于阈值”时，ECDF 比密度图更直接。
- **One distribution plot is evidence, not proof**：图形诊断需要和统计检验、领域知识共同使用。

## Anti-patterns
- **只用默认 bins**：双峰、偏态或长尾可能被分箱掩盖。
- **把 KDE 当作真实概率密度**：小样本和边界附近会产生误导。
- **仅凭接近直线宣称正态**：Q-Q 图仍需结合样本量、尾部和检验结果。
- **比较多组时使用不同轴范围**：会放大或缩小组间差异。
- **用面积未归一化的直方图叠加密度曲线**：两个纵轴含义不一致。

## Code Examples
```python
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

fig, axes = plt.subplots(2, 2, figsize=(6.5, 5), constrained_layout=True)

sns.histplot(data=x, bins="fd", stat="density", color="#4C78A8", ax=axes[0, 0])
sns.kdeplot(data=x, bw_adjust=1.0, color="#E45756", ax=axes[0, 0])
stats.probplot(x, dist="norm", plot=axes[0, 1])
sns.ecdfplot(x=x, color="#2FBE8F", ax=axes[1, 0])

sorted_x = np.sort(x)
axes[1, 1].plot(sorted_x, stats.norm.cdf(sorted_x, x.mean(), x.std(ddof=1)))
axes[1, 1].set(xlabel="Value", ylabel="Theoretical CDF")
```
- **What it demonstrates**：在同一分析中组合直方图、KDE、Q-Q 和累积分布视角。

## Reference Tables
| 研究问题 | 首选图 | 关键参数/检查 |
|---|---|---|
| 数值集中在哪些区间 | 直方图 | bins、频数/密度、统一范围 |
| 是否存在峰、偏态或长尾 | KDE + 直方图 | bandwidth、边界效应 |
| 是否接近指定理论分布 | Q-Q / P-P | 尾部、中心、参考线 |
| 低于某阈值的比例是多少 | ECDF | 阈值线、百分位 |
| 比较两组完整分布 | 重叠 ECDF 或分面直方图 | 样本量、同轴范围 |

## Worked Example
一组模型残差看起来近似钟形，但可能包含重尾。先用 Freedman–Diaconis 规则绘制直方图，再叠加两个带宽的 KDE；随后绘制正态 Q-Q 图，若中心贴近参考线但两端明显偏离，则说明主体近似正态而尾部更重；最后用 ECDF 标出 `±2σ` 阈值外的比例。结论应描述为“中心近似正态、尾部偏重”，而不是简单写“残差服从正态分布”。

## Key Takeaways
1. 单变量图的主要任务是揭示分布、异常值和理论假设。
2. bins 和 bandwidth 必须做敏感性检查。
3. Q-Q 图更关注尾部，P-P 图更关注累计概率主体。
4. ECDF 是解释阈值、百分位和组间分布差异的直接工具。
5. 图形诊断不能代替统计检验和领域判断。

## Connects To
- **Ch 4**：在单变量理解之后选择合适的双变量关系图。
- **Ch 8**：案例首先通过直方图检查观测值与模型估算值的分布。
