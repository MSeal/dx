from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXParcoordsChartConfig(DEXChartBase):
    class Config:
        fields = {"include": {"selected_dimensions"}}


class DEXParcoordsChartView(DEXView):
    chart_mode: Literal["parcoords"] = "parcoords"
    chart: DEXParcoordsChartConfig = Field(default_factory=DEXParcoordsChartConfig)
