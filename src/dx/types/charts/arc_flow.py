from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXArcFlowConfig(DEXChartBase):
    # see dx.types.charts._base.DEXChartBase for available fields and configs
    pass


class DEXArcFlowChartView(DEXView):
    chart_mode: Literal["arc_flow"] = "arc_flow"
    chart: DEXArcFlowConfig = Field(default_factory=DEXArcFlowConfig)
