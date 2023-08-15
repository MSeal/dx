from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXFunnelConfig(DEXChartBase):
    # see dx.types.charts._base.DEXChartBase for available fields and configs
    pass


class DEXFunnelChartView(DEXView):
    chart_mode: Literal["funnel"] = "funnel"
    chart: DEXFunnelConfig = Field(default_factory=DEXFunnelConfig)
