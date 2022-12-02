from typing import Literal

from pydantic import Field

from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView


class DEXWordcloudChartConfig(DEXChartBase):
    class Config:
        fields = {
            "text_data_format": {"include": True},
            "token_metric": {"include": True},
            "word_color": {"include": True},
            "word_data": {"include": True},
            "word_rotate": {"include": True},
        }


class DEXWordcloudChartView(DEXView):
    chart_mode: Literal["wordcloud"] = "wordcloud"
    chart: DEXWordcloudChartConfig = Field(default_factory=DEXWordcloudChartConfig)
