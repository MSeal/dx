from typing import Optional

from dx.plotting.utils import handle_view
from dx.types.charts.candlestick import DEXCandlestickChartView
from dx.types.charts.cumulative import DEXCumulativeChartView
from dx.types.charts.line_percent import DEXLinePercentChartView
from dx.types.charts.stacked_area import DEXStackedAreaChartView
from dx.types.charts.stacked_percent import DEXStackedPercentChartView

__all__ = [
    "candlestick",
    "cumulative",
    "line_percent",
    "stacked_area",
    "stacked_percent",
]


def sample_candlestick(df, **kwargs) -> Optional[DEXCandlestickChartView]:
    return handle_view(df, chart_mode="candlestick", **kwargs)


def candlestick(df, **kwargs) -> Optional[DEXCandlestickChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_candlestick(df, **kwargs)


def sample_cumulative(df, **kwargs) -> Optional[DEXCumulativeChartView]:
    return handle_view(df, chart_mode="cumulative", **kwargs)


def cumulative(df, **kwargs) -> Optional[DEXCumulativeChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_cumulative(df, **kwargs)


def sample_line_percent(df, **kwargs) -> Optional[DEXLinePercentChartView]:
    return handle_view(df, chart_mode="line_percent", **kwargs)


def line_percent(df, **kwargs) -> Optional[DEXLinePercentChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_line_percent(df, **kwargs)


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
