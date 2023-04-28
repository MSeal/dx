from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXForceDirectedNetworkConfig(DEXChartBase):
    # see dx.types.charts._base.DEXChartBase for available fields and configs
    pass


class DEXForceDirectedNetworkChartView(DEXView):
    chart_mode: Literal["force_directed_network"] = "force_directed_network"
    chart: DEXForceDirectedNetworkConfig = Field(default_factory=DEXForceDirectedNetworkConfig)
