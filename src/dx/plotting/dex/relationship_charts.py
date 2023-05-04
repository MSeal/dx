from typing import Callable, Dict, Optional

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
    "relationship_chart_functions",
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



def dendrogram(
    df,
    selected_dimensions: Union[List[str], str],
    hierarchy_type: options.DEXHierarchyType = "dendrogram",
    network_label: options.DEXNetworkLabelType = "none",
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXDendrogramChartView]:
    """
    Generates a DEX Dendrogram Diagram from the given DataFrame.

    Parameters
    ----------
    df: pd.DataFrame
        The DataFrame to plot.
    metric1: str
        The column for the size of the partitions
    selected_dimensions: Union[List[str], str]
        The columns(s) to use for the nesting.
    hierarchy_type: DEXHierarchyType
        The hierarchy type to use:
            - `"treemap"`
            - `"sunburst"`
            - `"partition"` (default)
            - `"dendrogram"`
    network_label: DEXNetworkLabelType
        Whether to show no labels (none), labels of equal size (static) or labels scaled to value (scaled)
    return_view: bool
        Whether to return a `DEXView` object instead of render.
    **kwargs
        Additional keyword arguments to pass to the view metadata.
    """
    raise_for_missing_columns(x, df.columns)

    if isinstance(selected_dimensions, str):
        selected_dimensions = [selected_dimensions]
    raise_for_missing_columns(selected_dimensions, df.columns)

    chart_settings = {
        "metric1": metric1,
        "selected_dimensions": selected_dimensions,
        "network_label": network_label,
        "hierarchy_type": hierarchy_type,
    }
    logger.debug(f"{chart_settings=}")
    return handle_view(
        df,
        chart_mode="hierarchy",
        chart=chart_settings,
        return_view=return_view,
        **kwargs,
    )

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


def relationship_chart_functions() -> Dict[str, Callable]:
    return {
        "adjacency_matrix": adjacency_matrix,
        "arc_flow": arc_flow,
        "dendrogram": dendrogram,
        "force_directed_network": force_directed_network,
        "sankey": sankey,
    }
