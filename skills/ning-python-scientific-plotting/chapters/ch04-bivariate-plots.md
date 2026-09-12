# Chapter 4: 双变量图形的绘制

## Core Idea
双变量图先按变量类型选择候选图：类别–连续用于组间比较，连续–连续用于趋势和相关结构，领域专用图则回答 ROC、生存、差异筛选等特定问题。尽量同时呈现摘要、不确定性与原始样本。

## Frameworks Introduced
- **变量类型优先法**：先判断离散/连续组合，再选图，而不是先选“好看的图”。
- **摘要 + 原始数据原则**：均值、中位数和误差区间用于概括，原始点用于展示样本量、偏态和异常值。
- **关系证据阶梯**：散点 → 拟合线 → 置信区间 → 边际分布；只增加研究问题需要的层。
- **领域专用图匹配**：ROC、生存曲线、火山图和子弹图只能用于其定义的问题。

## Key Concepts
- **误差线**：表示 SD、SE 或 CI，图注必须说明定义。
- **克利夫兰点图**：用点的位置比较类别数值，通常比柱长更易精确读取。
- **箱线图**：用四分位数、中位数、须和异常值概括分布。
- **小提琴图**：以核密度宽度展示分布形态。
- **云雨图**：组合半小提琴、区间/箱线和原始点。
- **边际组合图**：在散点主图旁添加两个变量各自的分布。
- **相关矩阵热力图**：用颜色编码多对变量的相关系数。
- **子弹图**：用实际值、目标值和等级区间表达阶段性绩效。

## Mental Models
- **Use position before area**：精确比较优先点位置或线位置，不优先面积和角度。
- **Show uncertainty with its definition**：没有定义的误差线没有完整统计含义。
- **Use lines only when order is meaningful**：无序类别不要用连线暗示连续过程。
- **Use density only with enough data**：小样本的提琴/KDE 容易制造伪结构。
- **Correlation is not causation**：拟合线描述关系，不替代因果设计。

## Anti-patterns
- **均值柱形图隐藏原始数据**：看不到样本量、偏态、多峰和异常值。
- **误差线未注明 SD/SE/CI**：读者无法解释区间。
- **饼图类别过多**：角度和面积难比较，优先排序点图或条形图。
- **散点重叠仍使用大而不透明的点**：应降低透明度、缩小点或改用 hexbin/二维密度。
- **跨面板轴范围不一致**：会制造不存在的视觉差异。

## Code Examples
```python
import matplotlib.pyplot as plt
import seaborn as sns

fig, axes = plt.subplots(1, 2, figsize=(6.8, 2.8), constrained_layout=True)

sns.violinplot(data=df, x="group", y="value", inner=None, cut=0, ax=axes[0])
sns.boxplot(data=df, x="group", y="value", width=0.22,
            boxprops={"facecolor": "white"}, ax=axes[0])
sns.stripplot(data=df, x="group", y="value", color="black", alpha=0.4, ax=axes[0])

sns.regplot(data=df, x="observed", y="predicted",
            scatter_kws={"s": 14, "alpha": 0.4}, ax=axes[1])
limits = [df[["observed", "predicted"]].min().min(),
          df[["observed", "predicted"]].max().max()]
axes[1].plot(limits, limits, "k--", linewidth=0.8, label="1:1")
axes[1].legend(frameon=False)
```
- **What it demonstrates**：类别–连续图展示分布和样本，连续–连续图展示关系和 1:1 参考线。

## Reference Tables
| 数据/问题 | 首选图 | 必须说明 |
|---|---|---|
| 多组中心值与区间 | 点图 + 误差线 | SD、SE 或 CI |
| 多组完整分布 | 箱线、提琴、云雨图 | 样本量、原始点 |
| 类别排序比较 | 克利夫兰点图、棒棒糖图 | 基准与排序依据 |
| 两连续变量关系 | 散点图 | 拟合、区间、相关系数 |
| 随时间变化 | 折线图 | 时间间隔、缺失值、区间 |
| 大量点重叠 | 透明散点、hexbin、二维密度 | 颜色条含义 |
| 多变量两两相关 | 相关矩阵热力图 | 系数类型与样本量 |
| 分类器阈值性能 | ROC | AUC、阳性类、置信区间 |
| 时间到事件 | 生存曲线 | 风险表、删失标记 |
| 效应与显著性 | 火山图 | fold-change 与 p 值阈值 |
| 实际值与目标值 | 子弹图 | 目标线和等级区间 |

## Worked Example
比较四种处理的响应值时，使用原始点叠加箱线或云雨图，并按中位数排序。若需报告模型估计，在旁边增加估计点和 95% CI，而不是再画均值柱形图。图注写明箱体、须、区间的定义和每组 `n`，让读者同时看到中心、离散、异常值与样本证据。

## Key Takeaways
1. 变量类型决定候选图，研究问题决定最终图。
2. 类别比较应展示位置、区间和样本，不只展示柱长。
3. 连续关系图要处理重叠、参考线和不确定性。
4. 连线必须对应真实顺序或连续过程。
5. 专用图不能脱离其领域定义使用。

## Connects To
- **Ch 3**：单变量分布帮助解释双变量关系。
- **Ch 8**：案例用相关性散点和多面板比较模型与观测值。
