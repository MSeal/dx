from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXSunburstConfig(DEXChartBase):
    # see dx.types.charts._base.DEXChartBase for available fields and configs
    pass


class DEXSunburstChartView(DEXView):
    chart_mode: Literal["sunburst"] = "sunburst"
    chart: DEXSunburstConfig = Field(default_factory=DEXSunburstConfig)
