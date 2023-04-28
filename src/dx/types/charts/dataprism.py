from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView

__all__ = ["DEXDataPrismChartView"]


class DEXDataPrismChartConfig(DEXChartBase):
    class Config:
        fields = {
            "suggestion_fields": {"include": True},
        }


class DEXDataPrismChartView(DEXView):
    chart_mode: Literal["dataprism"] = "dataprism"
    chart: DEXDataPrismChartConfig = Field(default_factory=DEXDataPrismChartConfig)
