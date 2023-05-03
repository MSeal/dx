from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXFlowDiagramConfig(DEXChartBase):
    # see dx.types.charts._base.DEXChartBase for available fields and configs
    pass


class DEXFlowDiagramChartView(DEXView):
    chart_mode: Literal["flow_diagram"] = "flow_diagram"
    chart: DEXFlowDiagramConfig = Field(default_factory=DEXFlowDiagramConfig)
