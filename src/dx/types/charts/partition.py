from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXPartitionConfig(DEXChartBase):
    # see dx.types.charts._base.DEXChartBase for available fields and configs
    pass


class DEXPartitionChartView(DEXView):
    chart_mode: Literal["partition"] = "partition"
    chart: DEXPartitionConfig = Field(default_factory=DEXPartitionConfig)
