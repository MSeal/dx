from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXGridConfig(DEXChartBase):
    pass


class DEXGridChartView(DEXView):
    chart_mode: Literal["grid"] = "grid"
    chart: DEXGridConfig = Field(default_factory=DEXGridConfig)
