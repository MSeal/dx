from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXStackedAreaConfig(DEXChartBase):
    # see dx.types.charts._base.DEXChartBase for available fields and configs
    pass


class DEXStackedAreaChartView(DEXView):
    chart_mode: Literal["stacked_area"] = "stacked_area"
    chart: DEXStackedAreaConfig = Field(default_factory=DEXStackedAreaConfig)
