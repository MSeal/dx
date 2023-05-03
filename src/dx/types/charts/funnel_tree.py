from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXFunnelTreeConfig(DEXChartBase):
    # see dx.types.charts._base.DEXChartBase for available fields and configs
    pass


class DEXFunnelTreeChartView(DEXView):
    chart_mode: Literal["funnel_tree"] = "funnel_tree"
    chart: DEXFunnelTreeConfig = Field(default_factory=DEXFunnelTreeConfig)
