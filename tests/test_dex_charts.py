"""Tests covering basic modeling for the various programmatic DEX functions.

As models and arguments are fleshed out, their associated test(s) should move from the `sample_*`
function to the primary function, and check for more specific attributes.
"""

import pandas as pd

from dx.plotting import dex
from dx.types import charts


class TestBasicCharts:
    def test_bar(self, sample_random_dataframe: pd.DataFrame):
        view = dex.basic_charts.sample_bar(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.bar.DEXBarChartView)
        assert view.chart_mode == "bar"

    def test_dataprism(self, sample_random_dataframe: pd.DataFrame):
        view = dex.basic_charts.sample_dataprism(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.dataprism.DEXDataPrismChartView)
        assert view.chart_mode == "dataprism"

    def test_line(self, sample_random_dataframe: pd.DataFrame):
        view = dex.basic_charts.sample_line(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.line.DEXLineChartView)
        assert view.chart_mode == "line"

    def test_pie(self, sample_random_dataframe: pd.DataFrame):
        view = dex.basic_charts.sample_pie(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.pie.DEXPieChartView)
        assert view.chart_mode == "pie"

    def test_scatter(self, sample_random_dataframe: pd.DataFrame):
        view = dex.basic_charts.sample_scatter(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.scatter.DEXScatterChartView)
        assert view.chart_mode == "scatter"

    def test_wordcloud(self, sample_random_dataframe: pd.DataFrame):
        view = dex.basic_charts.sample_wordcloud(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.wordcloud.DEXWordcloudChartView)
        assert view.chart_mode == "wordcloud"


class TestComparisonCharts:
    def test_connected_scatterplot(self, sample_random_dataframe: pd.DataFrame):
        view = dex.comparison_charts.connected_scatterplot(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.connected_scatter.DEXConnectedScatterChartView)
        assert view.chart_mode == "connectedscatter"

    def test_correlation_matrix(self, sample_random_dataframe: pd.DataFrame):
        view = dex.comparison_charts.correlation_matrix(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.correlation_matrix.DEXCorrelationMatrixChartView)
        assert view.chart_mode == "correlation_matrix"

    def test_diverging_bar(self, sample_random_dataframe: pd.DataFrame):
        view = dex.comparison_charts.diverging_bar(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.diverging_bar.DEXDivergingBarChartView)
        assert view.chart_mode == "diverging_bar"

    def test_dotplot(self, sample_random_dataframe: pd.DataFrame):
        view = dex.comparison_charts.dotplot(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.dotplot.DEXGenericDotPlotChartView)
        assert view.chart_mode == "dotplot"
        assert view.chart.bar_projection == "horizontal"

    def test_parallel_coordinates(self, sample_random_dataframe: pd.DataFrame):
        view = dex.comparison_charts.sample_parallel_coordinates(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.parcoords.DEXParallelCoordinatesChartView)
        assert view.chart_mode == "parcoords"

    def test_radar_plot(self, sample_random_dataframe: pd.DataFrame):
        view = dex.comparison_charts.sample_radar_plot(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.dotplot.DEXGenericDotPlotChartView)
        assert view.chart_mode == "dotplot"
        assert view.chart.bar_projection == "radial"

    def test_scatterplot_matrix(self, sample_random_dataframe: pd.DataFrame):
        view = dex.comparison_charts.sample_scatterplot_matrix(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.scatterplot_matrix.DEXScatterPlotMatrixChartView)
        assert view.chart_mode == "splom"


class TestFunnelCharts:
    def test_flow_diagram(self, sample_random_dataframe: pd.DataFrame):
        view = dex.funnel_charts.flow_diagram(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.flow_diagram.DEXFlowDiagramChartView)
        assert view.chart_mode == "flow_diagram"

    def test_funnel_chart(self, sample_random_dataframe: pd.DataFrame):
        view = dex.funnel_charts.funnel_chart(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.funnel_chart.DEXFunnelChartChartView)
        assert view.chart_mode == "funnel_chart"

    def test_funnel_sunburst(self, sample_random_dataframe: pd.DataFrame):
        view = dex.funnel_charts.funnel_sunburst(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.funnel_sunburst.DEXFunnelSunburstChartView)
        assert view.chart_mode == "funnel_sunburst"

    def test_funnel_tree(self, sample_random_dataframe: pd.DataFrame):
        view = dex.funnel_charts.funnel_tree(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.funnel_tree.DEXFunnelTreeChartView)
        assert view.chart_mode == "funnel_tree"

    def test_funnel(self, sample_random_dataframe: pd.DataFrame):
        view = dex.funnel_charts.funnel(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.funnel.DEXFunnelChartView)
        assert view.chart_mode == "funnel"


class TestMapsCharts:
    def test_choropleth(self, sample_random_dataframe: pd.DataFrame):
        view = dex.map_charts.sample_choropleth(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.choropleth.DEXChoroplethChartView)
        assert view.chart_mode == "choropleth"

    def test_tilemap(self, sample_random_dataframe: pd.DataFrame):
        view = dex.map_charts.sample_tilemap(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.tilemap.DEXTilemapChartView)
        assert view.chart_mode == "tilemap"


class TestPartToWholeCharts:
    def test_donut(self, sample_random_dataframe: pd.DataFrame):
        view = dex.part_to_whole_charts.donut(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.donut.DEXDonutChartView)
        assert view.chart_mode == "donut"

    def test_partition(self, sample_random_dataframe: pd.DataFrame):
        view = dex.part_to_whole_charts.partition(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.partition.DEXPartitionChartView)
        assert view.chart_mode == "partition"

    def test_sunburst(self, sample_random_dataframe: pd.DataFrame):
        view = dex.part_to_whole_charts.sunburst(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.sunburst.DEXSunburstChartView)
        assert view.chart_mode == "sunburst"

    def test_treemap(self, sample_random_dataframe: pd.DataFrame):
        view = dex.part_to_whole_charts.treemap(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.treemap.DEXTreemapChartView)
        assert view.chart_mode == "treemap"


class TestRelationshipCharts:
    def test_adjacency_matrix(self, sample_random_dataframe: pd.DataFrame):
        view = dex.relationship_charts.adjacency_matrix(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.adjacency_matrix.DEXAdjacencyMatrixChartView)
        assert view.chart_mode == "adjacency_matrix"

    def test_arc_flow(self, sample_random_dataframe: pd.DataFrame):
        view = dex.relationship_charts.arc_flow(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.arc_flow.DEXArcFlowChartView)
        assert view.chart_mode == "arc_flow"

    def test_dendrogram(self, sample_random_dataframe: pd.DataFrame):
        view = dex.relationship_charts.dendrogram(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.dendrogram.DEXDendrogramChartView)
        assert view.chart_mode == "dendrogram"

    def test_force_directed_network(self, sample_random_dataframe: pd.DataFrame):
        view = dex.relationship_charts.force_directed_network(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.force_directed_network.DEXForceDirectedNetworkChartView)
        assert view.chart_mode == "network"
        assert view.chart.network_type == "force"

    def test_sankey(self, sample_random_dataframe: pd.DataFrame):
        view = dex.relationship_charts.sankey(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.sankey.DEXSankeyChartView)
        assert view.chart_mode == "sankey"


class TestSummaryCharts:
    def test_bignumber(self, sample_random_dataframe: pd.DataFrame):
        view = dex.summary_charts.sample_big_number(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.bignumber.DEXBigNumberChartView)
        assert view.chart_mode == "bignumber"

    def test_boxplot(self, sample_random_dataframe: pd.DataFrame):
        view = dex.summary_charts.sample_boxplot(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.summary.DEXSummaryChartView)
        assert view.chart_mode == "summary"
        assert view.chart.summary_type == "boxplot"

    def test_dimension_matrix(self, sample_random_dataframe: pd.DataFrame):
        view = dex.summary_charts.sample_dimension_matrix(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.dimension_matrix.DEXDimensionMatrixChartView)
        assert view.chart_mode == "dimension_matrix"

    def test_heatmap(self, sample_random_dataframe: pd.DataFrame):
        view = dex.summary_charts.sample_heatmap(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.summary.DEXSummaryChartView)
        assert view.chart_mode == "summary"
        assert view.chart.summary_type == "heatmap"

    def test_hexbin(self, sample_random_dataframe: pd.DataFrame):
        view = dex.summary_charts.sample_hexbin(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.hexbin.DEXHexbinChartView)
        assert view.chart_mode == "hexbin"

    def test_histogram(self, sample_random_dataframe: pd.DataFrame):
        view = dex.summary_charts.sample_histogram(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.summary.DEXSummaryChartView)
        assert view.chart_mode == "summary"
        assert view.chart.summary_type == "histogram"

    def test_horizon(self, sample_random_dataframe: pd.DataFrame):
        view = dex.summary_charts.sample_horizon(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.summary.DEXSummaryChartView)
        assert view.chart_mode == "summary"
        assert view.chart.summary_type == "horizon"

    def test_ridgeline(self, sample_random_dataframe: pd.DataFrame):
        view = dex.summary_charts.sample_ridgeline(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.summary.DEXSummaryChartView)
        assert view.chart_mode == "summary"
        assert view.chart.summary_type == "ridgeline"

    def test_violin(self, sample_random_dataframe: pd.DataFrame):
        view = dex.summary_charts.sample_violin(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.summary.DEXSummaryChartView)
        assert view.chart_mode == "summary"
        assert view.chart.summary_type == "violin"


class TestTimeSeriesCharts:
    def test_candlestick(self, sample_random_dataframe: pd.DataFrame):
        view = dex.time_series_charts.sample_candlestick(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.candlestick.DEXCandlestickChartView)
        assert view.chart_mode == "candlestick"

    def test_cumulative(self, sample_random_dataframe: pd.DataFrame):
        view = dex.time_series_charts.sample_cumulative(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.cumulative.DEXCumulativeChartView)
        assert view.chart_mode == "cumulative"

    def test_line_percent(self, sample_random_dataframe: pd.DataFrame):
        view = dex.time_series_charts.sample_line_percent(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.line_percent.DEXLinePercentChartView)
        assert view.chart_mode == "line_percent"

    def test_stacked_area(self, sample_random_dataframe: pd.DataFrame):
        view = dex.time_series_charts.sample_stacked_area(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.stacked_area.DEXStackedAreaChartView)
        assert view.chart_mode == "stacked_area"

    def test_stacked_percent(self, sample_random_dataframe: pd.DataFrame):
        view = dex.time_series_charts.sample_stacked_percent(
            sample_random_dataframe,
            return_view=True,
        )
        assert isinstance(view, charts.stacked_percent.DEXStackedPercentChartView)
        assert view.chart_mode == "stacked_percent"
