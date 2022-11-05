from typing import Literal

from pydantic import Field

from dx.types.charts._configs import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXTilemapChartConfig(DEXChartBase):
    class Config:
        fields = {
            "map_mode": {"include": True},  # "tile"
            "layer_settings": {"include": True},
        }


class DEXTilemapChartView(DEXView):
    chart_type: Literal["tilemap"] = "tilemap"
    chart: DEXTilemapChartConfig = Field(default_factory=DEXTilemapChartConfig)
