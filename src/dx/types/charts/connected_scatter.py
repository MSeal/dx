from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXConnectedScatterConfig(DEXChartBase):
    # see dx.types.charts._base.DEXChartBase for available fields and configs
    pass


class DEXConnectedScatterChartView(DEXView):
    chart_mode: Literal["connected_scatter"] = "connected_scatter"
    chart: DEXConnectedScatterConfig = Field(default_factory=DEXConnectedScatterConfig)
