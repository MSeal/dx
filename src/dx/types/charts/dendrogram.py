from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXDendrogramConfig(DEXChartBase):
    # see dx.types.charts._base.DEXChartBase for available fields and configs
    pass


class DEXDendrogramChartView(DEXView):
    chart_mode: Literal["dendrogram"] = "dendrogram"
    chart: DEXDendrogramConfig = Field(default_factory=DEXDendrogramConfig)
