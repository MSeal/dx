from typing import Optional

from dx.plotting import dex
from dx.types.dex_metadata import DEXView


def get_chart_view(df, chart_mode: str, **kwargs) -> Optional[DEXView]:
    chart_modules = [
        dex.basic,
        dex.comparison,
        dex.funnel,
        dex.maps,
        dex.part_to_whole,
        dex.summary,
        dex.time_series,
    ]
    for chart_module in chart_modules:
        if chart_func := getattr(chart_module, chart_mode, None):
            return chart_func(df, return_view=True, **kwargs)
