from typing import Optional

from dx.plotting.utils import handle_view
from dx.types.charts.flow_diagram import DEXFlowDiagramChartView
from dx.types.charts.funnel import DEXFunnelChartView
from dx.types.charts.funnel_chart import DEXFunnelChartChartView
from dx.types.charts.funnel_sunburst import DEXFunnelSunburstChartView
from dx.types.charts.funnel_tree import DEXFunnelTreeChartView

__all__ = [
    "flow_diagram",
    "funnel",
    "funnel_chart",
    "funnel_sunburst",
    "funnel_tree",
]


def sample_flow_diagram(df, **kwargs) -> Optional[DEXFlowDiagramChartView]:
    return handle_view(df, chart_mode="flow_diagram", **kwargs)


def flow_diagram(df, **kwargs) -> Optional[DEXFlowDiagramChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_flow_diagram(df, **kwargs)


def sample_funnel_chart(df, **kwargs) -> Optional[DEXFunnelChartChartView]:
    return handle_view(df, chart_mode="funnel_chart", **kwargs)


def funnel_chart(df, **kwargs) -> Optional[DEXFunnelChartChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_funnel_chart(df, **kwargs)


def sample_funnel_sunburst(df, **kwargs) -> Optional[DEXFunnelSunburstChartView]:
    return handle_view(df, chart_mode="funnel_sunburst", **kwargs)


def funnel_sunburst(df, **kwargs) -> Optional[DEXFunnelSunburstChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_funnel_sunburst(df, **kwargs)


def sample_funnel_tree(df, **kwargs) -> Optional[DEXFunnelTreeChartView]:
    return handle_view(df, chart_mode="funnel_tree", **kwargs)


def funnel_tree(df, **kwargs) -> Optional[DEXFunnelTreeChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_funnel_tree(df, **kwargs)


def sample_funnel(df, **kwargs) -> Optional[DEXFunnelChartView]:
    return handle_view(df, chart_mode="funnel", **kwargs)


def funnel(df, **kwargs) -> Optional[DEXFunnelChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_funnel(df, **kwargs)
