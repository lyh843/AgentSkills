# Chapter 8: 学术图绘制案例

## Core Idea
论文配图应跟随研究流程，而不是各自孤立：先用分布图了解数据，再用关系图比较观测与模型结果，最后用综合指标图评价模型性能。

## Frameworks Introduced
- **三阶段图形叙事**：数据观察 → 相关性分析 → 模型精度评价。
- **一问一图**：每个阶段先写出要回答的问题，再选择能直接提供证据的图。
- **多面板同尺度比较**：多个模型或地物类型必须共享轴范围、统计标注和视觉样式。
- **从详细到综合**：散点图解释单个模型行为，泰勒图在模型数量较多时提供总体比较。

## Key Concepts
- **数据观察期**：用直方图或箱线图检查数值范围、频数、分布和异常值。
- **相关性分析**：用观测值–估算值散点、1:1 线、回归方程、`R²` 和 RMSE 检查模型行为。
- **模型精度评估**：结合相关系数、RMSE 和标准差进行综合比较。
- **多子图统一编码**：行列分别对应模型、地物类型或分析阶段，避免每个面板采用不同视觉语言。
- **蒸散发案例**：书中以 ET 观测值和 DNN、GBRT、LR、SVR 等模型估算值为例。

## Mental Models
- **Start with distribution before correlation**：分布范围和异常值会影响相关与回归解释。
- **Use 1:1 as the scientific reference**：预测–观测图不仅要有回归线，还要有理想一致线。
- **Use small multiples for fair comparison**：统一面板比把所有模型叠在一个坐标轴上更易比较。
- **Use summary plots after diagnostic plots**：Taylor 图不能替代对偏倚、异常值和局部误差的检查。

## Anti-patterns
- **跳过数据观察直接报告模型指标**：无法发现范围错误、异常值和分布偏移。
- **各模型使用自动轴范围**：视觉斜率和离散程度不能公平比较。
- **只展示相关系数**：高相关仍可能伴随系统偏倚和大 RMSE。
- **面板重复图例和标签**：浪费空间并削弱整体结构。
- **为了组合而组合**：多面板必须共享一个明确比较问题。

## Code Examples
```python
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

models = ["DNN", "GBRT", "LR", "SVR"]
fig, axes = plt.subplots(2, 2, figsize=(6.8, 6.0), sharex=True, sharey=True)

low = min(df["observed"].min(), df[models].min().min())
high = max(df["observed"].max(), df[models].max().max())

for ax, model in zip(axes.flat, models):
    sns.regplot(data=df, x="observed", y=model,
                scatter_kws={"s": 10, "alpha": 0.3}, ax=ax)
    ax.plot([low, high], [low, high], "k--", linewidth=0.8)
    rmse = np.sqrt(np.mean((df[model] - df["observed"]) ** 2))
    corr = df[["observed", model]].corr().iloc[0, 1]
    ax.text(0.04, 0.94, f"r={corr:.2f}\nRMSE={rmse:.2f}",
            transform=ax.transAxes, va="top")
    ax.set_title(model)
```
- **What it demonstrates**：统一坐标、统一统计标注和 1:1 参考线的模型多面板比较。

## Reference Tables
| 研究阶段 | 核心问题 | 推荐图 |
|---|---|---|
| 数据观察 | 数值范围、频数和异常值是什么 | 直方图、箱线图、ECDF |
| 模型关系 | 估算值是否跟随观测变化 | 散点 + 1:1 + 回归/指标 |
| 分组比较 | 模型在不同类别是否稳定 | 共享尺度多面板 |
| 多模型总评 | 哪个模型综合表现更好 | 泰勒图 + 指标表 |
| 时间误差 | 模型何时偏离观测 | 观测/估算折线与残差图 |

## Worked Example
书中的 ET 案例先用直方图比较观测值和多个模型估算值的分布，判断范围和频数是否相近；再按地物类型制作相关性散点多面板，统一显示回归关系、`R²`、RMSE 和 1:1 线；最后在模型较多时计算相关系数、RMSE 与标准差并绘制泰勒图。结论不是由单张图决定，而是由分布、局部关系和综合指标共同支持。

## Key Takeaways
1. 图形顺序应对应研究分析顺序。
2. 数据分布检查先于模型关系和精度评价。
3. 多模型面板必须共享尺度、样式和统计口径。
4. 相关、偏倚、RMSE 和离散程度要联合解释。
5. 综合图用于汇总，诊断图用于解释失败原因。

## Connects To
- **Ch 3**：用直方图和 ECDF 观察数据分布。
- **Ch 4**：用相关性散点和多面板分析模型关系。
- **Ch 7**：用泰勒图综合评价多个模型。
