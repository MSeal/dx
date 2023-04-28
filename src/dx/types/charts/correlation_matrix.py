from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXCorrelationMatrixConfig(DEXChartBase):
    pass


class DEXCorrelationMatrixChartView(DEXView):
    chart_mode: Literal["correlation_matrix"] = "correlation_matrix"
    chart: DEXCorrelationMatrixConfig = Field(default_factory=DEXCorrelationMatrixConfig)
