from typing import Optional

from dx.plotting.utils import handle_view
from dx.types.charts.candlestick import DEXCandlestickChartView
from dx.types.charts.cumulative import DEXCumulativeChartView
from dx.types.charts.line_percent import DEXLinePercentChartView


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
