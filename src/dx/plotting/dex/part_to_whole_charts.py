from typing import Callable, Dict, Optional

from dx.plotting.utils import handle_view
from dx.types.charts.donut import DEXDonutChartView
from dx.types.charts.hierarchy import DEXPartitionChartView
from dx.types.charts.hierarchy import DEXSunburstChartView
from dx.types.charts.hierarchy import DEXTreemapChartView

__all__ = [
    "donut",
    "partition",
    "sunburst",
    "treemap",
    "part_to_whole_chart_functions",
]


def sample_donut(df, **kwargs) -> Optional[DEXDonutChartView]:
    return handle_view(df, chart_mode="donut", **kwargs)


def donut(df, **kwargs) -> Optional[DEXDonutChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_donut(df, **kwargs)


def partition(
    df,
    metric1: str,
    selected_dimensions: Union[List[str], str],
    hierarchy_type: options.DEXHierarchyType = "partition",
    network_label: options.DEXNetworkLabelType = "none",
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXPartitionChartView]:
    """
    Generates a DEX Partition Diagram from the given DataFrame.

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

def sample_partition(df, **kwargs) -> Optional[DEXPartitionChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_partition(df, **kwargs)

def sunburst(
    df,
    metric1: str,
    selected_dimensions: Union[List[str], str],
    hierarchy_type: options.DEXHierarchyType = "sunburst",
    network_label: options.DEXNetworkLabelType = "none",
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXSunburstChartView]:
    """
    Generates a DEX Sunburst Diagram from the given DataFrame.

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

def sample_sunburst(df, **kwargs) -> Optional[DEXSunburstChartView]:
    return handle_view(df, chart_mode="sunburst", **kwargs)


def treemap(
    df,
    metric1: str,
    selected_dimensions: Union[List[str], str],
    hierarchy_type: options.DEXHierarchyType = "treemap",
    network_label: options.DEXNetworkLabelType = "none",
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXTreemapChartView]:
    """
    Generates a DEX Treemap Diagram from the given DataFrame.

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


def sample_treemap(df, **kwargs) -> Optional[DEXTreemapChartView]:
    return handle_view(df, chart_mode="treemap", **kwargs)


def part_to_whole_chart_functions() -> Dict[str, Callable]:
    return {
        "donut": donut,
        "partition": partition,
        "sunburst": sunburst,
        "treemap": treemap,
    }
