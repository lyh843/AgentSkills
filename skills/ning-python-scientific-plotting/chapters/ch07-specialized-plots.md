# Chapter 7: 其他类型图的绘制

## Core Idea
专用图形与特定统计问题绑定：Bland–Altman 检查一致性，配对图显示个体变化，泰勒图综合模型指标，森林图和漏斗图服务 Meta 分析，史密斯图服务阻抗匹配。先确认统计定义，再绘图。

## Frameworks Introduced
- **方法一致性框架**：Bland–Altman 以两次测量的均值为 x、差值为 y，报告偏倚和 95% 一致性界限。
- **配对证据框架**：保留同一对象前后或两条件间的连接，避免把配对数据当独立样本。
- **模型综合评价框架**：泰勒图同时编码相关系数、标准差和中心化均方根误差。
- **Meta 分析图形分工**：森林图展示效应量与 CI，漏斗图辅助检查小样本效应或发表偏倚。

## Key Concepts
- **Bias**：两种方法测量差值的平均值。
- **95% Limits of Agreement**：差值近似正态时为 `bias ± 1.96 × SD(diff)`。
- **配对图/前后图**：用线连接同一个体的两次观测。
- **韦恩图**：展示少量集合的交集与差集。
- **泰勒图**：把相关性、标准差和 RMSE 放在同一极坐标结构中。
- **森林图**：点表示效应估计，横线表示置信区间，汇总效应常用菱形表示。
- **漏斗图**：横轴通常为效应量，纵轴为标准误或精度。
- **史密斯图**：把归一化复阻抗映射到反射系数平面。

## Mental Models
- **Agreement is not correlation**：高度相关的两种方法仍可能存在系统偏倚。
- **Pairing is information**：配对关系本身是实验设计的一部分，不能在图中丢失。
- **Taylor is a dashboard, not a verdict**：综合图仍需分别解释相关性、离散程度和误差。
- **Funnel asymmetry has multiple causes**：不对称不自动等于发表偏倚。
- **Specialized plots require domain validation**：可视化代码不能替代领域统计分析。

## Anti-patterns
- **用相关系数替代一致性分析**：相关只反映共同变化，不反映可互换性。
- **Bland–Altman 不检查差值随均值变化**：异方差或比例偏倚会使固定 LoA 不合适。
- **配对样本只画两组箱线图**：个体变化方向被隐藏。
- **韦恩图展示许多集合**：区域数量迅速增加，改用 UpSet 类图形。
- **少于约 10 项研究时过度解释漏斗图**：书中提醒此时检验效能不足。
- **森林图只显示 p 值**：效应量和 CI 才是主要信息。

## Code Examples
```python
import numpy as np
import matplotlib.pyplot as plt

mean = (method_a + method_b) / 2
diff = method_a - method_b
bias = diff.mean()
sd = diff.std(ddof=1)
lower, upper = bias - 1.96 * sd, bias + 1.96 * sd

fig, ax = plt.subplots(figsize=(4.5, 3.2))
ax.scatter(mean, diff, s=18, alpha=0.6)
ax.axhline(bias, color="black", label=f"Bias = {bias:.2f}")
ax.axhline(lower, color="#4C78A8", linestyle="--")
ax.axhline(upper, color="#4C78A8", linestyle="--", label="95% LoA")
ax.set(xlabel="Mean of methods", ylabel="A - B")
ax.legend(frameon=False)
```
- **What it demonstrates**：从原始配对测量计算偏倚与一致性界限，而不是仅调用绘图函数。

## Reference Tables
| 研究问题 | 图形 | 核心量 |
|---|---|---|
| 两测量方法能否互换 | Bland–Altman | bias、LoA、趋势 |
| 同一个体前后变化 | 配对图/前后图 | 个体连线、差值 |
| 少量集合交集 | 韦恩图 | 交集与差集大小 |
| 多模型综合评价 | 泰勒图 | 相关、SD、RMSE |
| 多研究效应汇总 | 森林图 | 效应量、CI、权重 |
| 小样本效应/偏倚线索 | 漏斗图 | 效应量、标准误、对称性 |
| 传输线阻抗匹配 | 史密斯图 | 归一化阻抗、反射系数 |

## Worked Example
比较新仪器与标准仪器时，先画散点和相关性只能说明两者共同变化。随后计算每个样本的均值与差值，绘制 Bland–Altman 图；检查平均偏倚是否接近零、绝大多数点是否处于 LoA 内，以及差值是否随测量水平扩大。只有 LoA 在领域可接受范围内，才能讨论方法替代性。

## Key Takeaways
1. 一致性、相关性和显著性是不同问题。
2. 配对数据必须保留个体连接。
3. 泰勒图用于多模型综合比较，但要拆解指标解释。
4. 森林图展示效应与区间，漏斗图只提供偏倚线索。
5. 史密斯图属于电磁与射频工程专用工具。

## Connects To
- **Ch 4**：专用图建立在双变量关系和不确定性表达基础上。
- **Ch 8**：模型较多时使用泰勒图比较估算结果。
