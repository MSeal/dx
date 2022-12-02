from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXTilemapChartConfig(DEXChartBase):
    class Config:
        fields = {
            "map_mode": {"include": True},  # "tile"
            "layer_settings": {"include": True},
        }


class DEXTilemapChartView(DEXView):
    chart_mode: Literal["tilemap"] = "tilemap"
    chart: DEXTilemapChartConfig = Field(default_factory=DEXTilemapChartConfig)
