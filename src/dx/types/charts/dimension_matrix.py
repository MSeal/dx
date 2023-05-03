from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXDimensionMatrixConfig(DEXChartBase):
    # see dx.types.charts._base.DEXChartBase for available fields and configs
    pass


class DEXDimensionMatrixChartView(DEXView):
    chart_mode: Literal["dimension_matrix"] = "dimension_matrix"
    chart: DEXDimensionMatrixConfig = Field(default_factory=DEXDimensionMatrixConfig)
