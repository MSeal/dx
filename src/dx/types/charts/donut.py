from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXDonutConfig(DEXChartBase):
    # see dx.types.charts._base.DEXChartBase for available fields and configs
    pass


class DEXDonutChartView(DEXView):
    chart_mode: Literal["donut"] = "donut"
    chart: DEXDonutConfig = Field(default_factory=DEXDonutConfig)
