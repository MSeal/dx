from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXScatterPlotMatrixConfig(DEXChartBase):
    pass


class DEXScatterPlotMatrixChartView(DEXView):
    chart_mode: Literal["scatterplot_matrix"] = "scatterplot_matrix"
    chart: DEXScatterPlotMatrixConfig = Field(default_factory=DEXScatterPlotMatrixConfig)
