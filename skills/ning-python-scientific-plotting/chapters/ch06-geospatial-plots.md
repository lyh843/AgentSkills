# Chapter 6: 空间数据型图形的绘制

## Core Idea
空间图首先是地理数据分析，其次才是绘图。先确认数据类型、坐标参考系、投影与空间连接，再选择分级统计、气泡、连接线、等值线或子地图。

## Frameworks Introduced
- **空间绘图工作流**：读取 → 检查 CRS → 清洗几何 → 投影转换 → 属性/空间连接 → 选择地图类型 → 添加要素 → 输出。
- **变量–地图匹配**：连续率值用分级统计或等值线，绝对数量用比例符号，类别用类型地图，流动关系用连接线。
- **投影适配任务**：显示、距离、面积和方向不能由所有投影同时保持，应根据分析目标选择。
- **主图–子地图结构**：子地图用于放大局部、补充位置背景或处理离散区域，不应简单重复主图。

## Key Concepts
- **矢量数据**：点、线、面几何及属性，常见格式有 Shapefile、GeoJSON。
- **栅格数据**：规则网格像元，常用于遥感、地形和连续场。
- **CRS**：定义坐标如何对应地球位置的坐标参考系。
- **地理坐标系**：以经纬度表示位置，角度不是统一平面距离单位。
- **投影坐标系**：把地球表面映射到平面，用于距离、面积分析和制图。
- **分级统计地图**：按区域填色表示标准化连续属性。
- **双变量分级统计地图**：组合两个离散化连续变量的颜色类别。
- **气泡地图**：在地理位置上用符号面积编码绝对量。
- **连接线地图**：表示起点、终点、方向和流量。
- **Inset map**：嵌入主图的局部或概览地图。

## Mental Models
- **CRS before plot**：位置错位、比例异常或连接失败时，先检查 CRS，不先调坐标范围。
- **Use rates for areas, counts for symbols**：区域填色优先率值，绝对量优先比例符号。
- **Normalize visual density**：区域面积大不代表数据更重要。
- **Map is not the territory**：投影、分级和插值都会影响视觉结论，必须公开方法。

## Anti-patterns
- **经纬度直接计算距离或面积**：角度单位导致错误，应投影到适合的 CRS。
- **绝对数量直接做区域填色**：人口或面积规模会主导图形，应考虑率值或标准化指标。
- **彩虹色带表达连续量**：视觉顺序不均匀并产生伪边界。
- **不报告分级方法和断点**：相同数据会因分箱规则得到不同叙事。
- **底图、边界和注记压过数据层**：装饰不应抢占视觉层级。
- **子地图没有范围框或连接指示**：读者无法定位放大区域。

## Code Examples
```python
import geopandas as gpd
import matplotlib.pyplot as plt

regions = gpd.read_file("regions.geojson")
points = gpd.read_file("measurements.geojson")

regions = regions.to_crs("EPSG:3857")
points = points.to_crs(regions.crs)
joined = gpd.sjoin(regions, points, how="left", predicate="contains")

fig, ax = plt.subplots(figsize=(5.2, 4.2))
joined.plot(column="rate", cmap="YlGnBu", scheme="quantiles", k=5,
            edgecolor="white", linewidth=0.4, legend=True, ax=ax)
ax.set_axis_off()
fig.savefig("choropleth.pdf", bbox_inches="tight")
```
- **What it demonstrates**：统一 CRS 后执行空间连接，并用分位数分级绘制率值地图。

## Reference Tables
| 研究对象 | 推荐地图 | 数据处理要求 |
|---|---|---|
| 区域率值/指数 | 单变量分级统计地图 | 报告分级法和断点 |
| 两个区域指标 | 双变量分级统计地图 | 两变量分别分级，制作二维图例 |
| 地点绝对数量 | 气泡地图 | 面积按数值缩放，提供大小图例 |
| 地点类别 | 类型地图 | 离散色相和清晰图例 |
| 起终点流动 | 连接线地图 | 线宽、方向和重叠处理 |
| 连续空间场 | 等值线地图 | 插值方法、网格分辨率、色条 |
| 局部区域或离岛 | 子地图 | 主图范围框、连接线、统一样式 |

## Worked Example
绘制行政区疾病负担时，不能直接用病例数填色。先计算每十万人发病率，并投影到适合区域的等面积坐标系；按分位数或领域阈值分级，使用顺序色带。若还需表达病例总数，可叠加按面积缩放的气泡。图注同时说明 CRS、分级方法、时间范围和缺失值处理。

## Key Takeaways
1. CRS、投影和空间连接是地图可信度的基础。
2. 区域填色优先标准化率值，绝对量优先比例符号。
3. 分级断点和插值方法必须可复现。
4. 地图装饰服务于定位，不应压过数据层。
5. 子地图需要明确指出其对应的主图位置。

## Connects To
- **Ch 1**：地图同样遵循连续、发散和类别配色规则。
- **Ch 5**：气泡、等值线、矢量场和连接关系在空间坐标系中的应用。
