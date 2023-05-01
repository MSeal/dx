from typing import Optional

from dx.plotting.dex.basic import *
from dx.plotting.dex.comparison import *
from dx.plotting.dex.funnel import *
from dx.plotting.dex.maps import *
from dx.plotting.dex.part_to_whole import *
from dx.plotting.dex.summary import *
from dx.plotting.dex.time_series import *
from dx.types.dex_metadata import DEXView

chart_functions = {
    **basic_chart_functions(),
    **comparison_chart_functions(),
    **funnel_chart_functions(),
    **maps_chart_functions(),
    **part_to_whole_chart_functions(),
    **summary_chart_functions(),
    **time_series_chart_functions(),
}


def get_chart_view(df, chart_mode: str, **kwargs) -> Optional[DEXView]:
    chart_func = chart_functions.get(chart_mode)
    if chart_func is not None:
        return chart_func(df, return_view=True, **kwargs)
