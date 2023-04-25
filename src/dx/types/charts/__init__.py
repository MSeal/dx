from typing import Union

from pydantic import Field
from typing_extensions import Annotated

from dx.types.charts.bar import DEXBarChartView
from dx.types.charts.bignumber import DEXBigNumberChartView
from dx.types.charts.dataprism import DEXDataPrismChartView
from dx.types.charts.hexbin import DEXHexbinChartView
from dx.types.charts.line import DEXLineChartView
from dx.types.charts.parcoords import DEXParallelCoordinatesChartView
from dx.types.charts.pie import DEXPieChartView
from dx.types.charts.scatter import DEXScatterChartView
from dx.types.charts.summary import DEXSummaryChartView
from dx.types.charts.tilemap import DEXTilemapChartView
from dx.types.charts.wordcloud import DEXWordcloudChartView

basic_charts = Annotated[
    Union[
        DEXBarChartView,
        DEXLineChartView,
        DEXPieChartView,
        DEXScatterChartView,
        DEXTilemapChartView,
        DEXWordcloudChartView,
        DEXDataPrismChartView,
    ],
    Field(discriminator="chart_mode"),
]
comparison_charts = Annotated[
    Union[
        DEXBarChartView,
        DEXParallelCoordinatesChartView,
        DEXScatterChartView,
        # DEXScatterplotMatrixChartView,
        # DEXCorrelationMatrixChartView,
        # DEXDotPlotChartView,
        # DEXRadarPlotView,
        # DEXDivergingBarChartView,
    ],
    Field(discriminator="chart_mode"),
]

time_series_charts = [
    # DEXLineChartView,
    # DEXCumulativeChartView,
    # DEXStackedAreaChartView,
    # DEXLinePercentChartView,
    # DEXStackedPercentChartView,
    # DEXCandlestickChartView,
]

relationship_charts = [
    # DEXForceDirectedNetworkChartView,
    # DEXSankeyChartView,
    # DEXArcDiagramChartView,
    # DEXAdjacencyMatrixChartView,
    # DEXDendrogramChartView,
]

part_to_whole_charts = [
    DEXPieChartView,
    # DEXDonutChartView,
    # DEXSunburstChartView,
    # DEXTreemapChartView,
    # DEXPartitionChartView,
]

funnel_charts = [
    # DEXFunnelView,
    # DEXFunnelChartView,
    # DEXFunnelTreeChartView,
    # DEXFunnelSunburstChartView,
    # DEXFlowDiagramChartView,
]

summary_charts = Annotated[
    Union[
        DEXBigNumberChartView,
        DEXWordcloudChartView,
        # DEXDimensionMatrixChartView,
        DEXHexbinChartView,
        DEXSummaryChartView,
    ],
    Field(discriminator="chart_mode"),
]

map_charts = [
    # DEXChoroplethChartView,
    # DEXTilemapChartView,
]
