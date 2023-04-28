"""
Convenience functions to quickly create charts from a dataframe with no required chart configs.
"""

from typing import Optional

from dx.plotting.utils import handle_view
from dx.types.dex_metadata import DEXView


# ⛔
def sample_adjacency_matrix(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="adjacency_matrix", **kwargs)


# ⛔
def sample_arc_diagram(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="arc_diagram", **kwargs)


# ⛔
def sample_arc_flow(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="arc_flow", **kwargs)


# ✅
def sample_bar(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="bar", **kwargs)


# ⛔
def sample_big_number(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="big_number", **kwargs)


# ✅
def sample_boxplot(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="summary", chart={"summaryType": "boxplot"}, **kwargs)


# ⛔
def sample_candlestick(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="candlestick", **kwargs)


# ⛔
def sample_choropleth(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="choropleth", **kwargs)


# ✅
def sample_connected_scatterplot(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="connectedscatter", **kwargs)


# ⛔
def sample_correlation_matrix(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="correlation_matrix", **kwargs)


# ⛔
def sample_cumulative(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="cumulative", **kwargs)


# ?
def sample_dataprism(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="dataprism", **kwargs)


# ⛔
def sample_dendrogram(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="dendrogram", **kwargs)


# ⛔
def sample_dimension_matrix(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="dimension_matrix", **kwargs)


# ⛔
def sample_diverging_bar(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="diverging_bar", **kwargs)


# ⛔
def sample_donut(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="donut", **kwargs)


# ✅
def sample_dotplot(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="dotplot", **kwargs)


# ⛔
def sample_flow_diagram(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="flow_diagram", **kwargs)


# ✅
def sample_force_directed_network(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="network", chart={"networkType": "force"}, **kwargs)


# ⛔
def sample_funnel_chart(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="funnel_chart", **kwargs)


# ⛔
def sample_funnel_sunburst(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="funnel_sunburst", **kwargs)


# ⛔
def sample_funnel_tree(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="funnel_tree", **kwargs)


# ✅
def sample_funnel(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="funnel", **kwargs)


# ✅
def sample_heatmap(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="summary", chart={"summaryType": "heatmap"}, **kwargs)


# ✅
def sample_hexbin(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="hexbin", **kwargs)


# ✅
def sample_histogram(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="summary", chart={"summaryType": "histogram"}, **kwargs)


# ✅
def sample_horizon(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="summary", chart={"summaryType": "horizon"}, **kwargs)


# ⛔
def sample_line_percent(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="line_percent", **kwargs)


# ✅?
def sample_line(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="line", **kwargs)


# ✅
def sample_parallel_coordinates(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="parcoords", **kwargs)


# ⛔
def sample_partition(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="partition", **kwargs)


# ✅
def sample_pie(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="pie", **kwargs)


# ✅
def sample_radar_plot(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="dotplot", chart={"barProjection": "radial"}, **kwargs)


# ✅
def sample_ridgeline(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="summary", chart={"summaryType": "ridgeline"}, **kwargs)


# ⛔
def sample_sankey(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="sankey", **kwargs)


# ✅
def sample_scatter(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="scatter", **kwargs)


# ⛔
def sample_scatterplot_matrix(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="scatterplot_matrix", **kwargs)


# ⛔
def sample_stacked_area(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="stacked_area", **kwargs)


# ⛔
def sample_stacked_percent(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="stacked_percent", **kwargs)


# ⛔
def sample_sunburst(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="sunburst", **kwargs)


# ✅
def sample_tilemap(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="tilemap", **kwargs)


# ⛔
def sample_treemap(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="treemap", **kwargs)


# ✅
def sample_violin(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="summary", chart={"summaryType": "violin"}, **kwargs)


# ✅
def sample_wordcloud(df, **kwargs) -> Optional[DEXView]:
    return handle_view(df, chart_mode="wordcloud", **kwargs)
