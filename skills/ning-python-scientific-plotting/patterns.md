# Patterns

## Journal-First Figure Design
**When to use**: 准备论文正式插图时。
**How**: 读取目标期刊当前指南；确定栏宽、格式、DPI、字体和颜色模式；按最终尺寸创建 Figure；完成灰度和可读性检查后导出。
**Trade-offs**: 前期约束更多，但避免定稿时大规模返工。

## One Question, One Figure
**When to use**: 决定图是否进入正文时。
**How**: 为每张图写出一个明确研究问题；删除不能直接提供证据的装饰层和重复面板。
**Trade-offs**: 图数量更少，但每张图的信息职责更清晰。

## Distribution Diagnostic Stack
**When to use**: 建模前检查连续变量或残差时。
**How**: 依次查看直方图、KDE、Q-Q/P-P 和 ECDF；改变 bins/bandwidth 做敏感性检查；结合统计检验与领域知识下结论。
**Trade-offs**: 比单张直方图耗时，但能发现尾部、多峰和阈值问题。

## Summary Plus Raw Data
**When to use**: 比较类别组的连续测量值时。
**How**: 使用原始点叠加箱线、区间或云雨图；报告每组样本量；在图注中定义误差线。
**Trade-offs**: 样本很多时会拥挤，需要透明度、抽样或密度表达。

## Fair Small Multiples
**When to use**: 比较多个模型、组别、地区或时间段时。
**How**: 共享轴范围、颜色映射、统计口径和面板尺寸；只保留一个公共图例；按自然比较顺序排列面板。
**Trade-offs**: 单个面板空间较小，但跨组比较更可靠。

## Observed-vs-Predicted Panel
**When to use**: 评价连续预测模型时。
**How**: 画观测–预测散点、1:1 线、拟合线；标注相关、RMSE 和样本量；检查偏倚、异方差和异常值。
**Trade-offs**: 指标较多时图面会拥挤，应把次要统计量放入表格。

## Visual Channel Budget
**When to use**: 需要在一个图中表达三个以上变量时。
**How**: 最重要变量映射 x/y；连续次要量映射颜色或面积；类别映射色相或标记；删除重复编码。
**Trade-offs**: 会舍弃部分维度，但降低认知负担和图例复杂度。

## Projection-Aware Mapping
**When to use**: 绘制或分析任何空间数据时。
**How**: 检查所有图层 CRS；根据面积、距离或显示任务选择投影；统一 CRS 后再连接和绘图；记录投影与分级方法。
**Trade-offs**: 需要额外地理知识，但避免位置、面积和距离错误。

## Rate Fill, Count Symbol
**When to use**: 同时表达区域指标和绝对数量时。
**How**: 用标准化率值做区域填色，用按面积缩放的气泡表示绝对数量，并分别提供颜色和大小图例。
**Trade-offs**: 双重编码较复杂，必须保持颜色和符号视觉层级分离。

## Agreement Before Replacement
**When to use**: 判断两种测量方法是否可替代时。
**How**: 计算差值、偏倚和 LoA；画 Bland–Altman 图；检查比例偏倚和领域可接受范围，不仅报告相关系数。
**Trade-offs**: 结论可能比相关分析更保守，但统计问题正确。

## Diagnostic-to-Summary Narrative
**When to use**: 组织论文整套模型评价图时。
**How**: 先用分布图检查输入和输出，再用关系图诊断各模型，最后用泰勒图或指标表汇总。
**Trade-offs**: 需要多张互补图，但避免用单一综合指标掩盖失败模式。

## Reproducible Export
**When to use**: 交付最终插图时。
**How**: 集中管理 rcParams；固定 Figure 尺寸；保存矢量母版和所需位图；记录软件版本、字体、DPI 与输出命令。
**Trade-offs**: 初始设置稍多，但可批量更新并保证整篇论文一致。
