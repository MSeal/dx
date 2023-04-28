import pandas as pd

from dx.plotting.utils import handle_view


class TestBasicCharts:
    def test_bar(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="bar",
            return_view=True,
        )
        assert view.chart_mode == "bar"

    def test_dataprism(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="dataprism",
            return_view=True,
        )
        assert view.chart_mode == "dataprism"

    def test_scatter(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="scatter",
            return_view=True,
        )
        assert view.chart_mode == "scatter"

    def test_wordcloud(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="wordcloud",
            return_view=True,
        )
        assert view.chart_mode == "wordcloud"


class TestComparisonCharts:
    def test_connected_scatterplot(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="connected_scatter",
            return_view=True,
        )
        assert view.chart_mode == "connected_scatter"

    def test_correlation_matrix(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="correlation_matrix",
            return_view=True,
        )
        assert view.chart_mode == "correlation_matrix"

    def test_diverging_bar(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="diverging_bar",
            return_view=True,
        )
        assert view.chart_mode == "diverging_bar"

    def test_dotplot(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="dotplot",
            return_view=True,
        )
        assert view.chart_mode == "dotplot"

    def test_parallel_coordinates(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="parcoords",
            return_view=True,
        )
        assert view.chart_mode == "parcoords"

    def test_radar_plot(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="dotplot",
            chart={"bar_projection": "radial"},
            return_view=True,
        )
        assert view.chart_mode == "dotplot"
        assert view.chart.bar_projection == "radial"

    def test_scatterplot_matrix(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="scatterplot_matrix",
            return_view=True,
        )
        assert view.chart_mode == "scatterplot_matrix"


class TestFunnelCharts:
    def test_flow_diagram(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="flow_diagram",
            return_view=True,
        )
        assert view.chart_mode == "flow_diagram"

    def test_funnel_chart(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="funnel_chart",
            return_view=True,
        )
        assert view.chart_mode == "funnel_chart"

    def test_funnel_sunburst(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="funnel_sunburst",
            return_view=True,
        )
        assert view.chart_mode == "funnel_sunburst"

    def test_funnel_tree(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="funnel_tree",
            return_view=True,
        )
        assert view.chart_mode == "funnel_tree"

    def test_funnel(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="funnel",
            return_view=True,
        )
        assert view.chart_mode == "funnel"


class TestMapsCharts:
    def test_choropleth(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="choropleth",
            return_view=True,
        )
        assert view.chart_mode == "choropleth"

    def test_tilemap(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="tilemap",
            return_view=True,
        )
        assert view.chart_mode == "tilemap"


class TestPartToWholeCharts:
    def test_donut(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="donut",
            return_view=True,
        )
        assert view.chart_mode == "donut"

    def test_pie(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="pie",
            return_view=True,
        )
        assert view.chart_mode == "pie"

    def test_partition(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="partition",
            return_view=True,
        )
        assert view.chart_mode == "partition"

    def test_sunburst(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="sunburst",
            return_view=True,
        )
        assert view.chart_mode == "sunburst"

    def test_treemap(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="treemap",
            return_view=True,
        )
        assert view.chart_mode == "treemap"


class TestRelationshipCharts:
    def test_adjacency_matrix(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="adjacency_matrix",
            return_view=True,
        )
        assert view.chart_mode == "adjacency_matrix"

    def test_arc_flow(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="arc_flow",
            return_view=True,
        )
        assert view.chart_mode == "arc_flow"

    def test_dendrogram(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="dendrogram",
            return_view=True,
        )
        assert view.chart_mode == "dendrogram"

    def test_force_directed_network(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="network",
            chart={"network_type": "force"},
            return_view=True,
        )
        assert view.chart_mode == "network"
        assert view.chart.network_type == "force"

    def test_sankey(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="sankey",
            return_view=True,
        )
        assert view.chart_mode == "sankey"


class TestSummaryCharts:
    def test_bignumber(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="bignumber",
            return_view=True,
        )
        assert view.chart_mode == "bignumber"

    def test_boxplot(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="summary",
            chart={"summary_type": "boxplot"},
            return_view=True,
        )
        assert view.chart_mode == "summary"
        assert view.chart.summary_type == "boxplot"

    def test_dimension_matrix(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="dimension_matrix",
            return_view=True,
        )
        assert view.chart_mode == "dimension_matrix"

    def test_heatmap(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="summary",
            chart={"summary_type": "heatmap"},
            return_view=True,
        )
        assert view.chart_mode == "summary"
        assert view.chart.summary_type == "heatmap"

    def test_hexbin(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="hexbin",
            return_view=True,
        )
        assert view.chart_mode == "hexbin"

    def test_histogram(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="summary",
            chart={"summary_type": "histogram"},
            return_view=True,
        )
        assert view.chart_mode == "summary"
        assert view.chart.summary_type == "histogram"

    def test_horizon(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="summary",
            chart={"summary_type": "horizon"},
            return_view=True,
        )
        assert view.chart_mode == "summary"
        assert view.chart.summary_type == "horizon"

    def test_ridgeline(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="summary",
            chart={"summary_type": "ridgeline"},
            return_view=True,
        )
        assert view.chart_mode == "summary"
        assert view.chart.summary_type == "ridgeline"

    def test_violin(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="summary",
            chart={"summary_type": "violin"},
            return_view=True,
        )
        assert view.chart_mode == "summary"
        assert view.chart.summary_type == "violin"


class TestTimeSeriesCharts:
    def test_candlestick(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="candlestick",
            return_view=True,
        )
        assert view.chart_mode == "candlestick"

    def test_cumulative(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="cumulative",
            return_view=True,
        )
        assert view.chart_mode == "cumulative"

    def test_line_percent(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="line_percent",
            return_view=True,
        )
        assert view.chart_mode == "line_percent"

    def test_line(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="line",
            return_view=True,
        )
        assert view.chart_mode == "line"

    def test_stacked_area(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="stacked_area",
            return_view=True,
        )
        assert view.chart_mode == "stacked_area"

    def test_stacked_percent(self, sample_random_dataframe: pd.DataFrame):
        view = handle_view(
            sample_random_dataframe,
            chart_mode="stacked_percent",
            return_view=True,
        )
        assert view.chart_mode == "stacked_percent"
