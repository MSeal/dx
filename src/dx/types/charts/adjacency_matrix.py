from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXAdjacencyMatrixConfig(DEXChartBase):
    # see dx.types.charts._base.DEXChartBase for available fields and configs
    pass


class DEXAdjacencyMatrixChartView(DEXView):
    chart_mode: Literal["adjacency_matrix"] = "adjacency_matrix"
    chart: DEXAdjacencyMatrixConfig = Field(default_factory=DEXAdjacencyMatrixConfig)
