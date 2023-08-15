from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXDivergingBarConfig(DEXChartBase):
    pass


class DEXDivergingBarChartView(DEXView):
    chart_mode: Literal["diverging_bar"] = "diverging_bar"
    chart: DEXDivergingBarConfig = Field(default_factory=DEXDivergingBarConfig)
