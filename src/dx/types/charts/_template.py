"""Template for new Chart types. Do not use this file directly."""


from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXTemplateConfig(DEXChartBase):
    # see dx.types.charts._base.DEXChartBase for available fields and configs
    pass


class DEXTemplateChartView(DEXView):
    chart_mode: Literal["template"] = "template"
    chart: DEXTemplateConfig = Field(default_factory=DEXTemplateConfig)
