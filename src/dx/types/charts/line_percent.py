from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXLinePercentConfig(DEXChartBase):
    # see dx.types.charts._base.DEXChartBase for available fields and configs
    pass


class DEXLinePercentChartView(DEXView):
    chart_mode: Literal["line_percent"] = "line_percent"
    chart: DEXLinePercentConfig = Field(default_factory=DEXLinePercentConfig)
