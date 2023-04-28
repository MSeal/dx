from typing import Optional

from dx.plotting.utils import handle_view
from dx.types.charts.adjacency_matrix import DEXAdjacencyMatrixChartView
from dx.types.charts.arc_flow import DEXArcFlowChartView
from dx.types.charts.dendrogram import DEXDendrogramChartView
from dx.types.charts.force_directed_network import DEXForceDirectedNetworkChartView
from dx.types.charts.sankey import DEXSankeyChartView

__all__ = [
    "adjacency_matrix",
    "arc_flow",
    "dendrogram",
    "force_directed_network",
    "sankey",
]


def sample_adjacency_matrix(df, **kwargs) -> Optional[DEXAdjacencyMatrixChartView]:
    return handle_view(df, chart_mode="adjacency_matrix", **kwargs)


def adjacency_matrix(df, **kwargs) -> Optional[DEXAdjacencyMatrixChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_adjacency_matrix(df, **kwargs)


def sample_arc_flow(df, **kwargs) -> Optional[DEXArcFlowChartView]:
    return handle_view(df, chart_mode="arc_flow", **kwargs)


def arc_flow(df, **kwargs) -> Optional[DEXArcFlowChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_arc_flow(df, **kwargs)


def sample_dendrogram(df, **kwargs) -> Optional[DEXDendrogramChartView]:
    return handle_view(df, chart_mode="dendrogram", **kwargs)


def dendrogram(df, **kwargs) -> Optional[DEXDendrogramChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_dendrogram(df, **kwargs)


def sample_force_directed_network(df, **kwargs) -> Optional[DEXForceDirectedNetworkChartView]:
    return handle_view(df, chart_mode="network", chart={"network_type": "force"}, **kwargs)


def force_directed_network(df, **kwargs) -> Optional[DEXForceDirectedNetworkChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_force_directed_network(df, **kwargs)


def sample_sankey(df, **kwargs) -> Optional[DEXSankeyChartView]:
    return handle_view(df, chart_mode="sankey", **kwargs)


def sankey(df, **kwargs) -> Optional[DEXSankeyChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_sankey(df, **kwargs)
