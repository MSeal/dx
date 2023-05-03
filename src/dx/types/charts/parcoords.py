from typing import List, Literal, Optional

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXParallelCoordinatesChartConfig(DEXChartBase):
    selected_dimensions: Optional[List[str]] = Field(alias="selectedDimensions")


class DEXParallelCoordinatesChartView(DEXView):
    chart_mode: Literal["parcoords"] = "parcoords"
    chart: DEXParallelCoordinatesChartConfig = Field(
        default_factory=DEXParallelCoordinatesChartConfig
    )
