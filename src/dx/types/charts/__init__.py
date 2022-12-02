from ._base import *
from .bar import *
from .line import *
from .options import *
from .parcoords import *
from .pie import *
from .scatter import *
from .summary import *
from .tilemap import *
from .violin import *
from .wordcloud import *

basic_charts = [
    DEXBarChartView,
    DEXLineChartView,
    DEXPieChartView,
    DEXScatterChartView,
    DEXTilemapChartView,
    DEXViolinChartView,
    DEXWordcloudChartView,
]
comparison_charts = [
    DEXBarChartView,
    DEXParcoordsChartView,
    DEXScatterChartView,
    # DEXScatterplotMatrixChartView,
    # DEXCorrelationMatrixChartView,
    # DEXDotPlotChartView,
    # DEXRadarPlotView,
    # DEXDivergingBarChartView,
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
summary_charts = [
    # DEXBigNumberChartView,
    DEXWordcloudChartView,
    # DEXDimensionMatrixChartView,
    DEXViolinChartView,
    # DEXBoxPlotChartView,
    # DEXHeatmapChartView,
    # DEXHistogramChartView,
    # DEXRidgelineChartView,
    # DEXHorizonChartView,
    # DEXHexbinChartView,
]
map_charts = [
    # DEXChoroplethChartView,
    DEXTilemapChartView,
]
