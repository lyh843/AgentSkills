# Chapter 2: 绘制工具及其重要特征

## Core Idea
Matplotlib 提供底层控制，Seaborn 提供统计语义，ProPlot 简化出版级布局，SciencePlots 提供期刊风格。选择最少但足够的工具，并始终保留对 Matplotlib 对象的控制。

## Frameworks Introduced
- **Figure–Axes–Artist 层级**：Figure 是画布，Axes 是独立绘图区，线、文字、图例等是 Artist。
  - When to use: 定位样式设置应该作用于整张图、某个子图还是单个元素时。
  - How: 用 `fig` 管理整体尺寸和保存，用 `ax` 管理坐标与数据层，用对象方法修改具体元素。
- **面向对象绘图模式**：优先 `fig, ax = plt.subplots()` 和 `ax.*`，避免在复杂图中混用隐式状态接口。
- **统计语义层**：Seaborn 根据 tidy data 中的 `x`、`y`、`hue`、`style`、`size` 映射变量，Matplotlib 负责最终微调。
- **样式上下文**：全局统一论文样式；只有在局部图确实需要不同风格时才使用临时 context。

## Key Concepts
- **zorder**：控制图层前后顺序，数值越大越靠前。
- **Scale**：线性、对数等轴比例决定数据到视觉位置的映射。
- **Major/Minor ticks**：主刻度承担读数，次刻度提供辅助尺度。
- **Data/Axes/Figure coordinates**：数据坐标、子图相对坐标和画布相对坐标适用于不同标注需求。
- **Axes-level function**：绘制到指定 `ax`，适合自定义布局。
- **Figure-level function**：自行管理 Figure 和分面，适合快速生成 FacetGrid 类结果。
- **FacetGrid/PairGrid/JointGrid**：按类别、变量组合或边际分布组织多个统计图。
- **SciencePlots style**：通过 Matplotlib style 系统应用学术或期刊主题。

## Mental Models
- **Use Seaborn for semantics, Matplotlib for control**：先让 Seaborn 完成统计映射，再通过 `ax` 精修。
- **Layout before decoration**：先确定图幅、子图网格、共享轴和颜色条位置，再设置颜色与标注。
- **One source of style truth**：字体、字号、线宽等放在统一 `rcParams` 或样式文件中。
- **Explicit axes scale to complexity**：图越复杂，越应该显式持有 `fig` 和每个 `ax`。

## Anti-patterns
- **复杂图中混用 `plt.*` 和 `ax.*`**：容易把标题、刻度或图例加到错误子图。
- **绘图后才决定布局**：临时挪动图例和颜色条会造成不一致和遮挡。
- **依赖库的默认版本行为**：ProPlot、SciencePlots 等 API 会更新；生成 skill 时应以项目实际版本测试。
- **每幅图重复设置几十个参数**：应把稳定的出版规范集中到样式配置。
- **为了风格同时叠加多个主题库**：设置相互覆盖，难以定位最终值。

## Code Examples
```python
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use(["science", "no-latex"])
sns.set_context("paper")

fig, axes = plt.subplots(1, 2, figsize=(6.8, 2.8), constrained_layout=True)
sns.scatterplot(data=df, x="x", y="y", hue="group", ax=axes[0])
sns.boxplot(data=df, x="group", y="value", ax=axes[1])

for ax in axes:
    ax.tick_params(direction="in")
    ax.spines[["top", "right"]].set_visible(False)

handles, labels = axes[0].get_legend_handles_labels()
axes[0].legend_.remove()
fig.legend(handles, labels, frameon=False, loc="upper center", ncol=3)
fig.savefig("multi-panel.pdf", bbox_inches="tight")
```
- **What it demonstrates**：统一样式、显式子图对象、共享图例和出版级矢量输出。

## Reference Tables
| 工具 | 优先使用场景 | 保留的控制层 |
|---|---|---|
| Matplotlib | 任意静态图、精细排版、定制 Artist | 全部底层控制 |
| Seaborn | 分布、关系、分类统计、分面 | 返回或访问 Matplotlib Axes |
| ProPlot | 复杂多子图、统一 format、颜色条和图例布局 | 基于 Matplotlib 的扩展接口 |
| SciencePlots | 快速套用学术/期刊风格 | Matplotlib style 与 rcParams |

| 需求 | 推荐入口 |
|---|---|
| 单图或自定义网格 | `plt.subplots()` + axes-level functions |
| 按类别分面 | `relplot()`、`catplot()`、`displot()` 或 `FacetGrid` |
| 变量两两关系 | `pairplot()` / `PairGrid` |
| 主图加边际分布 | `jointplot()` / `JointGrid` |
| 稳定复用的出版风格 | `.mplstyle` 文件或集中 `rcParams` |

## Worked Example
制作四面板模型比较图时，先按目标双栏宽度创建 2×2 Axes，并共享坐标范围；每个面板调用同一个绘图函数，只传入数据子集和标题；从第一个 Axes 收集图例句柄，在 Figure 层创建一次公共图例；最后统一添加面板编号、对齐轴标签并保存为 PDF。这样避免四段近似代码产生样式漂移。

## Key Takeaways
1. Matplotlib 的对象层级是所有精细控制的基础。
2. Seaborn 负责统计语义，不替代 Matplotlib 的出版调整。
3. 多子图应先设计布局，再绘制内容。
4. 统一样式应集中管理，而不是复制到每个脚本。
5. 依赖主题库时记录版本，并在升级后重新核对输出。

## Connects To
- **Ch 1**：把规范、字体、配色和输出格式落实为配置。
- **Ch 8**：通过统一函数与多子图布局完成整篇论文的图形叙事。

