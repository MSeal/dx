from typing import Literal

from dx.types.dex_metadata import DEXView


class DEXSummaryChartView(DEXView):
    chart_mode: Literal["summary"] = "summary"
