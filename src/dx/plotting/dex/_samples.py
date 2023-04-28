"""
Convenience functions to quickly create charts from a dataframe with no required chart configs.
"""

from typing import Optional

from dx.plotting.utils import handle_view
from dx.types import charts


# ⛔
def sample_adjacency_matrix(df, **kwargs) -> Optional[charts.DEXAdjacencyMatrixChartView]:
    return handle_view(df, chart_mode="adjacency_matrix", **kwargs)


# ⛔
def sample_arc_flow(df, **kwargs) -> Optional[charts.DEXArcFlowChartView]:
    return handle_view(df, chart_mode="arc_flow", **kwargs)


# ✅
def sample_bar(df, **kwargs) -> Optional[charts.DEXBarChartView]:
    return handle_view(df, chart_mode="bar", **kwargs)


# ⛔
def sample_big_number(df, **kwargs) -> Optional[charts.DEXBigNumberChartView]:
    return handle_view(df, chart_mode="bignumber", **kwargs)


# ✅
def sample_boxplot(df, **kwargs) -> Optional[charts.DEXSummaryChartView]:
    return handle_view(df, chart_mode="summary", chart={"summary_type": "boxplot"}, **kwargs)


# ⛔
def sample_candlestick(df, **kwargs) -> Optional[charts.DEXCandlestickChartView]:
    return handle_view(df, chart_mode="candlestick", **kwargs)


# ⛔
def sample_choropleth(df, **kwargs) -> Optional[charts.DEXChoroplethChartView]:
    return handle_view(df, chart_mode="choropleth", **kwargs)


# ✅
def sample_connected_scatterplot(df, **kwargs) -> Optional[charts.DEXConnectedScatterChartView]:
    return handle_view(df, chart_mode="connected_scatter", **kwargs)


# ⛔
def sample_correlation_matrix(df, **kwargs) -> Optional[charts.DEXCorrelationMatrixChartView]:
    return handle_view(df, chart_mode="correlation_matrix", **kwargs)


# ⛔
def sample_cumulative(df, **kwargs) -> Optional[charts.DEXCumulativeChartView]:
    return handle_view(df, chart_mode="cumulative", **kwargs)


# ?
def sample_dataprism(df, **kwargs) -> Optional[charts.DEXDataPrismChartView]:
    return handle_view(df, chart_mode="dataprism", **kwargs)


# ⛔
def sample_dendrogram(df, **kwargs) -> Optional[charts.DEXDendrogramChartView]:
    return handle_view(df, chart_mode="dendrogram", **kwargs)


# ⛔
def sample_dimension_matrix(df, **kwargs) -> Optional[charts.DEXDimensionMatrixChartView]:
    return handle_view(df, chart_mode="dimension_matrix", **kwargs)


# ⛔
def sample_diverging_bar(df, **kwargs) -> Optional[charts.DEXDivergingBarChartView]:
    return handle_view(df, chart_mode="diverging_bar", **kwargs)


# ⛔
def sample_donut(df, **kwargs) -> Optional[charts.DEXDonutChartView]:
    return handle_view(df, chart_mode="donut", **kwargs)


# ✅
def sample_dotplot(df, **kwargs) -> Optional[charts.DEXDotPlotChartView]:
    return handle_view(df, chart_mode="dotplot", **kwargs)


# ⛔
def sample_flow_diagram(df, **kwargs) -> Optional[charts.DEXFlowDiagramChartView]:
    return handle_view(df, chart_mode="flow_diagram", **kwargs)


# ✅
def sample_force_directed_network(
    df, **kwargs
) -> Optional[charts.DEXForceDirectedNetworkChartView]:
    return handle_view(df, chart_mode="network", chart={"network_type": "force"}, **kwargs)


# ⛔
def sample_funnel_chart(df, **kwargs) -> Optional[charts.DEXFunnelChartChartView]:
    return handle_view(df, chart_mode="funnel_chart", **kwargs)


# ⛔
def sample_funnel_sunburst(df, **kwargs) -> Optional[charts.DEXFunnelSunburstChartView]:
    return handle_view(df, chart_mode="funnel_sunburst", **kwargs)


# ⛔
def sample_funnel_tree(df, **kwargs) -> Optional[charts.DEXFunnelTreeChartView]:
    return handle_view(df, chart_mode="funnel_tree", **kwargs)


# ✅
def sample_funnel(df, **kwargs) -> Optional[charts.DEXFunnelChartView]:
    return handle_view(df, chart_mode="funnel", **kwargs)


# ✅
def sample_heatmap(df, **kwargs) -> Optional[charts.DEXSummaryChartView]:
    return handle_view(df, chart_mode="summary", chart={"summary_type": "heatmap"}, **kwargs)


# ✅
def sample_hexbin(df, **kwargs) -> Optional[charts.DEXHexbinChartView]:
    return handle_view(df, chart_mode="hexbin", **kwargs)


# ✅
def sample_histogram(df, **kwargs) -> Optional[charts.DEXSummaryChartView]:
    return handle_view(df, chart_mode="summary", chart={"summary_type": "histogram"}, **kwargs)


# ✅
def sample_horizon(df, **kwargs) -> Optional[charts.DEXSummaryChartView]:
    return handle_view(df, chart_mode="summary", chart={"summary_type": "horizon"}, **kwargs)


# ⛔
def sample_line_percent(df, **kwargs) -> Optional[charts.DEXLinePercentChartView]:
    return handle_view(df, chart_mode="line_percent", **kwargs)


# ✅?
def sample_line(df, **kwargs) -> Optional[charts.DEXLineChartView]:
    return handle_view(df, chart_mode="line", **kwargs)


# ✅
def sample_parallel_coordinates(df, **kwargs) -> Optional[charts.DEXParallelCoordinatesChartView]:
    return handle_view(df, chart_mode="parcoords", **kwargs)


# ⛔
def sample_partition(df, **kwargs) -> Optional[charts.DEXPartitionChartView]:
    return handle_view(df, chart_mode="partition", **kwargs)


# ✅
def sample_pie(df, **kwargs) -> Optional[charts.DEXPieChartView]:
    return handle_view(df, chart_mode="pie", **kwargs)


# ✅
def sample_radar_plot(df, **kwargs) -> Optional[charts.DEXRadarPlotChartView]:
    return handle_view(df, chart_mode="dotplot", chart={"bar_projection": "radial"}, **kwargs)


# ✅
def sample_ridgeline(df, **kwargs) -> Optional[charts.DEXSummaryChartView]:
    return handle_view(df, chart_mode="summary", chart={"summary_type": "ridgeline"}, **kwargs)


# ⛔
def sample_sankey(df, **kwargs) -> Optional[charts.DEXSankeyChartView]:
    return handle_view(df, chart_mode="sankey", **kwargs)


# ✅
def sample_scatter(df, **kwargs) -> Optional[charts.DEXScatterChartView]:
    return handle_view(df, chart_mode="scatter", **kwargs)


# ⛔
def sample_scatterplot_matrix(df, **kwargs) -> Optional[charts.DEXScatterPlotMatrixChartView]:
    return handle_view(df, chart_mode="scatterplot_matrix", **kwargs)


# ⛔
def sample_stacked_area(df, **kwargs) -> Optional[charts.DEXStackedAreaChartView]:
    return handle_view(df, chart_mode="stacked_area", **kwargs)


# ⛔
def sample_stacked_percent(df, **kwargs) -> Optional[charts.DEXStackedPercentChartView]:
    return handle_view(df, chart_mode="stacked_percent", **kwargs)


# ⛔
def sample_sunburst(df, **kwargs) -> Optional[charts.DEXSunburstChartView]:
    return handle_view(df, chart_mode="sunburst", **kwargs)


# ✅
def sample_tilemap(df, **kwargs) -> Optional[charts.DEXTilemapChartView]:
    return handle_view(df, chart_mode="tilemap", **kwargs)


# ⛔
def sample_treemap(df, **kwargs) -> Optional[charts.DEXTreemapChartView]:
    return handle_view(df, chart_mode="treemap", **kwargs)


# ✅
def sample_violin(df, **kwargs) -> Optional[charts.DEXSummaryChartView]:
    return handle_view(df, chart_mode="summary", chart={"summary_type": "violin"}, **kwargs)


# ✅
def sample_wordcloud(df, **kwargs) -> Optional[charts.DEXWordcloudChartView]:
    return handle_view(df, chart_mode="wordcloud", **kwargs)
