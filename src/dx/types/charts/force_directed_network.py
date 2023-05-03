from typing import Literal

from pydantic import Field

from dx.types.charts import options
from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXForceDirectedNetworkConfig(DEXChartBase):
    # see dx.types.charts._base.DEXChartBase for available fields and configs
    network_type: options.DEXNetworkType = Field(
        alias="networkType",
        default=options.DEXNetworkType.force,
    )
    pass


class DEXForceDirectedNetworkChartView(DEXView):
    chart_mode: Literal["network"] = "network"
    chart: DEXForceDirectedNetworkConfig = Field(default_factory=DEXForceDirectedNetworkConfig)
