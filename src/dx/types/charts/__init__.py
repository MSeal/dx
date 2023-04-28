from typing import Union

from pydantic import Field
from typing_extensions import Annotated

from dx.types.charts import bar
from dx.types.charts import bignumber
from dx.types.charts import dataprism
from dx.types.charts import hexbin
from dx.types.charts import line
from dx.types.charts import parcoords
from dx.types.charts import pie
from dx.types.charts import scatter
from dx.types.charts import summary
from dx.types.charts import tilemap
from dx.types.charts import wordcloud

__all__ = [
    *bar.__all__,
    *bignumber.__all__,
    *dataprism.__all__,
    *hexbin.__all__,
    *line.__all__,
    *parcoords.__all__,
    *pie.__all__,
    *scatter.__all__,
    *summary.__all__,
    *tilemap.__all__,
    *wordcloud.__all__,
]

basic_charts = Annotated[
    Union[
        bar.DEXBarChartView,
        line.DEXLineChartView,
        pie.DEXPieChartView,
        scatter.DEXScatterChartView,
        tilemap.DEXTilemapChartView,
        wordcloud.DEXWordcloudChartView,
        dataprism.DEXDataPrismChartView,
    ],
    Field(discriminator="chart_mode"),
]
comparison_charts = Annotated[
    Union[
        bar.DEXBarChartView,
        parcoords.DEXParallelCoordinatesChartView,
        scatter.DEXScatterChartView,
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
    pie.DEXPieChartView,
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
        bignumber.DEXBigNumberChartView,
        wordcloud.DEXWordcloudChartView,
        # DEXDimensionMatrixChartView,
        hexbin.DEXHexbinChartView,
        summary.DEXSummaryChartView,
    ],
    Field(discriminator="chart_mode"),
]

map_charts = [
    # DEXChoroplethChartView,
    # DEXTilemapChartView,
]
