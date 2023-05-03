from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXBigNumberChartConfig(DEXChartBase):
    class Config:
        fields = {
            "dim1": {"include": True},
            "metric1": {"include": True},
            "combination_mode": {"include": True},
            "sparkchart": {"include": True},
            "second_metric": {"include": True},
            "second_metric_comparison": {"include": True},
        }


class DEXBigNumberChartView(DEXView):
    chart_mode: Literal["bignumber"] = "bignumber"
    chart: DEXBigNumberChartConfig = Field(default_factory=DEXBigNumberChartConfig)
