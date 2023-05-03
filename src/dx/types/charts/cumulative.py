from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXCumulativeConfig(DEXChartBase):
    pass


class DEXCumulativeChartView(DEXView):
    chart_mode: Literal["cumulative"] = "cumulative"
    chart: DEXCumulativeConfig = Field(default_factory=DEXCumulativeConfig)
