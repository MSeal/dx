from typing import Literal, Optional

from pydantic import Field

from dx.types.charts import options
from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXConnectedScatterConfig(DEXChartBase):
    csp_order: Optional[str] = Field(alias="cspOrder")
    line_smoothing: Optional[options.DEXLineSmoothing] = Field(alias="lineSmoothing")
    metric1: str
    metric2: str


class DEXConnectedScatterChartView(DEXView):
    chart_mode: Literal["connectedscatter"] = "connectedscatter"
    chart: DEXConnectedScatterConfig = Field(default_factory=DEXConnectedScatterConfig)
