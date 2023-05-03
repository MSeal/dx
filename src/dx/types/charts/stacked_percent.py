from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXStackedPercentConfig(DEXChartBase):
    # see dx.types.charts._base.DEXChartBase for available fields and configs
    pass


class DEXStackedPercentChartView(DEXView):
    chart_mode: Literal["stacked_percent"] = "stacked_percent"
    chart: DEXStackedPercentConfig = Field(default_factory=DEXStackedPercentConfig)
