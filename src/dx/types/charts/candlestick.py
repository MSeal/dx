from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXCandlestickConfig(DEXChartBase):
    # see dx.types.charts._base.DEXChartBase for available fields and configs
    pass


class DEXCandlestickChartView(DEXView):
    chart_mode: Literal["candlestick"] = "candlestick"
    chart: DEXCandlestickConfig = Field(default_factory=DEXCandlestickConfig)
