from typing import Literal

from pydantic import Field

from dx.types.charts._configs import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXParcoordsChartConfig(DEXChartBase):
    class Config:
        fields = {"include": {"selected_dimensions"}}


class DEXParcoordsChartView(DEXView):
    chart_type: Literal["parcoords"] = "parcoords"
    chart: DEXParcoordsChartConfig = Field(default_factory=DEXParcoordsChartConfig)
