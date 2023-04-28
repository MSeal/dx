from typing import Optional

from dx.plotting.utils import handle_view
from dx.types.charts.donut import DEXDonutChartView
from dx.types.charts.partition import DEXPartitionChartView
from dx.types.charts.stacked_area import DEXStackedAreaChartView
from dx.types.charts.stacked_percent import DEXStackedPercentChartView
from dx.types.charts.sunburst import DEXSunburstChartView
from dx.types.charts.treemap import DEXTreemapChartView


def sample_donut(df, **kwargs) -> Optional[DEXDonutChartView]:
    return handle_view(df, chart_mode="donut", **kwargs)


def donut(df, **kwargs) -> Optional[DEXDonutChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_donut(df, **kwargs)


def sample_partition(df, **kwargs) -> Optional[DEXPartitionChartView]:
    return handle_view(df, chart_mode="partition", **kwargs)


def partition(df, **kwargs) -> Optional[DEXPartitionChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_partition(df, **kwargs)


def sample_sunburst(df, **kwargs) -> Optional[DEXSunburstChartView]:
    return handle_view(df, chart_mode="sunburst", **kwargs)


def sunburst(df, **kwargs) -> Optional[DEXSunburstChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_sunburst(df, **kwargs)


def sample_treemap(df, **kwargs) -> Optional[DEXTreemapChartView]:
    return handle_view(df, chart_mode="treemap", **kwargs)


def treemap(df, **kwargs) -> Optional[DEXTreemapChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_treemap(df, **kwargs)


def sample_stacked_area(df, **kwargs) -> Optional[DEXStackedAreaChartView]:
    return handle_view(df, chart_mode="stacked_area", **kwargs)


def stacked_area(df, **kwargs) -> Optional[DEXStackedAreaChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_stacked_area(df, **kwargs)


def sample_stacked_percent(df, **kwargs) -> Optional[DEXStackedPercentChartView]:
    return handle_view(df, chart_mode="stacked_percent", **kwargs)


def stacked_percent(df, **kwargs) -> Optional[DEXStackedPercentChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_stacked_percent(df, **kwargs)
