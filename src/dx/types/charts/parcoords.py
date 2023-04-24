from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXParallelCoordinatesChartConfig(DEXChartBase):
    class Config:
        fields = {"include": {"selected_dimensions"}}


class DEXParallelCoordinatesChartView(DEXView):
    chart_mode: Literal["parcoords"] = "parcoords"
    chart: DEXParallelCoordinatesChartConfig = Field(
        default_factory=DEXParallelCoordinatesChartConfig
    )
