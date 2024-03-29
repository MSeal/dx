from typing import Callable, Dict, Optional

import pandas as pd
import structlog

from dx.plotting.utils import handle_view, raise_for_missing_columns
from dx.types.charts import options
from dx.types.charts.bignumber import DEXBigNumberChartView
from dx.types.charts.dimension_matrix import DEXDimensionMatrixChartView
from dx.types.charts.hexbin import DEXHexbinChartView
from dx.types.charts.summary import (
    DEXBoxplotChartView,
    DEXHeatmapChartView,
    DEXHistogramChartView,
    DEXHorizonChartView,
    DEXRidgelineChartView,
    DEXSummaryChartView,
    DEXViolinChartView,
)

logger = structlog.get_logger()

__all__ = [
    "bignumber",
    "boxplot",
    "dimension_matrix",
    "heatmap",
    "hexbin",
    "histogram",
    "horizon",
    "ridgeline",
    "violin",
    "summary_chart_functions",
]


def summary(
    df: pd.DataFrame,
    split_by: str,
    metric: str,
    summary_type: options.DEXSummaryType,
    chart_params: Optional[dict] = None,
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXSummaryChartView]:
    """Generates a DEX summary plot from a given DataFrame.

    Parameters
    ----------
    df: pd.DataFrame
        The DataFrame to plot.
    split_by: str
        The column to use for splitting the data.
    metric: str
        The column to use to show distribution and density.
    summary_type: DEXSummaryType
        The type of summary chart to show.
    chart_params: Optional[dict]
        Additional parameters to pass to the chart.
    return_view: bool
        Whether to return a `DEXView` object instead of render.
    **kwargs
        Additional keyword arguments to pass to the view metadata.
    """
    raise_for_missing_columns([split_by, metric], df.columns)

    chart_params = chart_params or {}
    chart_settings = {
        "dim1": split_by,
        "metric1": metric,
        "summary_type": summary_type,
        **chart_params,
    }

    return handle_view(
        df,
        chart_mode="summary",
        chart=chart_settings,
        return_view=return_view,
        **kwargs,
    )


def sample_boxplot(df, **kwargs) -> Optional[DEXSummaryChartView]:
    return handle_view(df, chart_mode="summary", chart={"summary_type": "boxplot"}, **kwargs)


def boxplot(
    df: pd.DataFrame,
    split_by: str,
    metric: str,
    show_outliers: bool = False,
    column_sort_order: options.DEXSortColumnsByOrder = "asc",
    column_sort_type: options.DEXSortColumnsByType = "string",
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXBoxplotChartView]:
    """
    Generates a DEX boxplot from the given DataFrame.

    Parameters
    ----------
    df: pd.DataFrame
        The DataFrame to plot.
    split_by: str
        The column to use for splitting the data.
    metric: str
        The column to use to show distribution and density.
    show_outliers: bool
        False: boxplot whiskers go to min/max
        True: boxplot whiskers go to 1.5x interquartile range with outliers shown individually
    column_sort_order: DEXSortColumnsByOrder
        The order to sort the columns by. (`"asc"` or `"desc"`)
    column_sort_type: DEXSortColumnsByType
        The type of sorting to use. (`"number"`, `"string"`, or `"date"`)
    return_view: bool
        Whether to return a `DEXView` object instead of render.
    **kwargs
        Additional keyword arguments to pass to the view metadata.
    """
    if str(column_sort_order).lower() == "asc":
        sort_order = "desc"
    elif str(column_sort_order).lower() == "desc":
        sort_order = "asc"
    chart_params = dict(
        boxplot_outliers=show_outliers,
        sort_columns_by=f"{sort_order}-col-{column_sort_type}",
    )
    return summary(
        df,
        split_by=split_by,
        metric=metric,
        summary_type="boxplot",
        chart_params=chart_params,
        return_view=return_view,
        **kwargs,
    )


def sample_big_number(df, **kwargs) -> Optional[DEXBigNumberChartView]:
    return handle_view(df, chart_mode="bignumber", **kwargs)


def bignumber(
    df: pd.DataFrame,
    split_by: str,
    metric: str,
    second_metric: Optional[str] = None,
    second_metric_comparison: options.DEXBigNumberComparison = "raw",
    combination_mode: options.DEXCombinationMode = "avg",
    sparkchart: options.DEXBigNumberSparklines = "none",
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXBigNumberChartView]:
    """
    Generates a DEX big number from the given DataFrame.

    Parameters
    ----------
    df: pd.DataFrame
        The DataFrame to plot.
    split_by: str
        The column to use for splitting the data.
    metric: str
        The column to use to show distribution and density.
    second_metric: str
        The column to use to show a second metric.
    second_metric_comparison: DEXBigNumberComparison
        The comparison to use for the second metric. (`"raw"`, `"percent"`, or `"change"`)
    combination_mode: DEXCombinationMode
        The combination mode to use. (`"avg"`, `"sum"`, `"min"`, or `"max"`)
    sparkchart: DEXBigNumberSparklines
        The sparkline type to use. (`"none"`, `"line"`, or `"bar"`)
    return_view: bool
        Whether to return a `DEXView` object instead of render.
    **kwargs
        Additional keyword arguments to pass to the view metadata.
    """
    raise_for_missing_columns([split_by, metric, combination_mode], df.columns)

    chart_settings = {
        "dim1": split_by,
        "metric1": metric,
        "combination_mode": combination_mode,
        "sparkchart": sparkchart,
    }

    if second_metric is not None:
        chart_settings.update(
            {
                "second_metric": second_metric,
                "second_metric_comparison": second_metric_comparison,
            }
        )

    return handle_view(
        df,
        chart_mode="bignumber",
        chart=chart_settings,
        return_view=return_view,
        **kwargs,
    )


def sample_dimension_matrix(df, **kwargs) -> Optional[DEXDimensionMatrixChartView]:
    return handle_view(df, chart_mode="dimension_matrix", **kwargs)


def dimension_matrix(df, **kwargs) -> Optional[DEXDimensionMatrixChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_dimension_matrix(df, **kwargs)


def sample_heatmap(df, **kwargs) -> Optional[DEXSummaryChartView]:
    return handle_view(df, chart_mode="summary", chart={"summary_type": "heatmap"}, **kwargs)


def heatmap(
    df: pd.DataFrame,
    split_by: str,
    metric: str,
    bins: int = 30,
    column_sort_order: options.DEXSortColumnsByOrder = "asc",
    column_sort_type: options.DEXSortColumnsByType = "string",
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXHeatmapChartView]:
    """
    Generates a DEX heatmap plot from the given DataFrame.

    Parameters
    ----------
    df: pd.DataFrame
        The DataFrame to plot.
    split_by: str
        The column to use for splitting the data.
    metric: str
        The column to use to show distribution and density.
    bins: int
        The number of bins to use for the heatmap plot.
    column_sort_order: DEXSortColumnsByOrder
        The order to sort the columns by. (`"asc"` or `"desc"`)
    column_sort_type: DEXSortColumnsByType
        The type of sorting to use. (`"number"`, `"string"`, or `"date"`)
    return_view: bool
        Whether to return a `DEXView` object instead of render.
    **kwargs
        Additional keyword arguments to pass to the view metadata.
    """
    if str(column_sort_order).lower() == "asc":
        sort_order = "desc"
    elif str(column_sort_order).lower() == "desc":
        sort_order = "asc"
    chart_params = dict(
        summary_bins=bins,
        sort_columns_by=f"{sort_order}-col-{column_sort_type}",
    )
    return summary(
        df,
        split_by=split_by,
        metric=metric,
        summary_type="heatmap",
        chart_params=chart_params,
        return_view=return_view,
        **kwargs,
    )


def sample_hexbin(df, **kwargs) -> Optional[DEXHexbinChartView]:
    return handle_view(df, chart_mode="hexbin", **kwargs)


def hexbin(
    df: pd.DataFrame,
    x: str,
    y: str,
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXHexbinChartView]:
    """
    Generates a DEX hexbin from the given DataFrame.

    Parameters
    ----------
    df: pd.DataFrame
        The DataFrame to plot.
    x: str
        The column to use for the x-axis.
    y: str
        The column to use for the y-axis.
    return_view: bool
        Whether to return a `DEXView` object instead of render.
    **kwargs
        Additional keyword arguments to pass to the view metadata.
    """
    raise_for_missing_columns([x, y], df.columns)

    chart_settings = {
        "metric1": x,
        "metric2": y,
    }

    return handle_view(
        df,
        chart_mode="hexbin",
        chart=chart_settings,
        return_view=return_view,
        **kwargs,
    )


def sample_horizon(df, **kwargs) -> Optional[DEXSummaryChartView]:
    return handle_view(df, chart_mode="summary", chart={"summary_type": "horizon"}, **kwargs)


def sample_histogram(df, **kwargs) -> Optional[DEXSummaryChartView]:
    return handle_view(df, chart_mode="summary", chart={"summary_type": "histogram"}, **kwargs)


def histogram(
    df: pd.DataFrame,
    split_by: str,
    metric: str,
    bins: int = 30,
    column_sort_order: options.DEXSortColumnsByOrder = "asc",
    column_sort_type: options.DEXSortColumnsByType = "string",
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXHistogramChartView]:
    """
    Generates a DEX histogram plot from the given DataFrame.

    Parameters
    ----------
    df: pd.DataFrame
        The DataFrame to plot.
    split_by: str
        The column to use for splitting the data.
    metric: str
        The column to use to show distribution and density.
    bins: int
        The number of bins to use for the histogram plot.
    column_sort_order: DEXSortColumnsByOrder
        The order to sort the columns by. (`"asc"` or `"desc"`)
    column_sort_type: DEXSortColumnsByType
        The type of sorting to use. (`"number"`, `"string"`, or `"date"`)
    return_view: bool
        Whether to return a `DEXView` object instead of render.
    **kwargs
        Additional keyword arguments to pass to the view metadata.
    """
    if str(column_sort_order).lower() == "asc":
        sort_order = "desc"
    elif str(column_sort_order).lower() == "desc":
        sort_order = "asc"
    chart_params = dict(
        summary_bins=bins,
        sort_columns_by=f"{sort_order}-col-{column_sort_type}",
    )
    return summary(
        df,
        split_by=split_by,
        metric=metric,
        summary_type="histogram",
        chart_params=chart_params,
        return_view=return_view,
        **kwargs,
    )


def horizon(
    df: pd.DataFrame,
    split_by: str,
    metric: str,
    bins: int = 30,
    column_sort_order: options.DEXSortColumnsByOrder = "asc",
    column_sort_type: options.DEXSortColumnsByType = "string",
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXHorizonChartView]:
    """
    Generates a DEX horizon plot from the given DataFrame.

    Parameters
    ----------
    df: pd.DataFrame
        The DataFrame to plot.
    split_by: str
        The column to use for splitting the data.
    metric: str
        The column to use to show distribution and density.
    bins: int
        The number of bins to use for the horizon plot.
    column_sort_order: DEXSortColumnsByOrder
        The order to sort the columns by. (`"asc"` or `"desc"`)
    column_sort_type: DEXSortColumnsByType
        The type of sorting to use. (`"number"`, `"string"`, or `"date"`)
    return_view: bool
        Whether to return a `DEXView` object instead of render.
    **kwargs
        Additional keyword arguments to pass to the view metadata.
    """
    if str(column_sort_order).lower() == "asc":
        sort_order = "desc"
    elif str(column_sort_order).lower() == "desc":
        sort_order = "asc"
    chart_params = dict(
        summary_bins=bins,
        sort_columns_by=f"{sort_order}-col-{column_sort_type}",
    )
    return summary(
        df,
        split_by=split_by,
        metric=metric,
        summary_type="horizon",
        chart_params=chart_params,
        return_view=return_view,
        **kwargs,
    )


def sample_ridgeline(df, **kwargs) -> Optional[DEXSummaryChartView]:
    return handle_view(df, chart_mode="summary", chart={"summary_type": "ridgeline"}, **kwargs)


def ridgeline(
    df: pd.DataFrame,
    split_by: str,
    metric: str,
    bins: int = 30,
    column_sort_order: options.DEXSortColumnsByOrder = "asc",
    column_sort_type: options.DEXSortColumnsByType = "string",
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXRidgelineChartView]:
    """
    Generates a DEX ridgeline plot from the given DataFrame.

    Parameters
    ----------
    df: pd.DataFrame
        The DataFrame to plot.
    split_by: str
        The column to use for splitting the data.
    metric: str
        The column to use to show distribution and density.
    bins: int
        The number of bins to use for the ridgeline plot.
    column_sort_order: DEXSortColumnsByOrder
        The order to sort the columns by. (`"asc"` or `"desc"`)
    column_sort_type: DEXSortColumnsByType
        The type of sorting to use. (`"number"`, `"string"`, or `"date"`)
    return_view: bool
        Whether to return a `DEXView` object instead of render.
    **kwargs
        Additional keyword arguments to pass to the view metadata.
    """
    if str(column_sort_order).lower() == "asc":
        sort_order = "desc"
    elif str(column_sort_order).lower() == "desc":
        sort_order = "asc"
    chart_params = dict(
        summary_bins=bins,
        sort_columns_by=f"{sort_order}-col-{column_sort_type}",
    )
    return summary(
        df,
        split_by=split_by,
        metric=metric,
        summary_type="ridgeline",
        chart_params=chart_params,
        return_view=return_view,
        **kwargs,
    )


def sample_violin(df, **kwargs) -> Optional[DEXSummaryChartView]:
    return handle_view(df, chart_mode="summary", chart={"summary_type": "violin"}, **kwargs)


def violin(
    df: pd.DataFrame,
    split_by: str,
    metric: str,
    bins: int = 30,
    show_interquartile_range: bool = False,
    column_sort_order: options.DEXSortColumnsByOrder = "asc",
    column_sort_type: options.DEXSortColumnsByType = "string",
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXViolinChartView]:
    """
    Generates a DEX violin plot from the given DataFrame.

    Parameters
    ----------
    df: pd.DataFrame
        The DataFrame to plot.
    split_by: str
        The column to use for splitting the data.
    metric: str
        The column to use to show distribution and density.
    bins: int
        The number of bins to use for the violin plot.
    show_interquartile_range: bool
        Whether to show the interquartile range.
    column_sort_order: DEXSortColumnsByOrder
        The order to sort the columns by. (`"asc"` or `"desc"`)
    column_sort_type: DEXSortColumnsByType
        The type of sorting to use. (`"number"`, `"string"`, or `"date"`)
    return_view: bool
        Whether to return a `DEXView` object instead of render.
    **kwargs
        Additional keyword arguments to pass to the view metadata.
    """
    if str(column_sort_order).lower() == "asc":
        sort_order = "desc"
    elif str(column_sort_order).lower() == "desc":
        sort_order = "asc"
    chart_params = dict(
        summary_bins=bins,
        sort_columns_by=f"{sort_order}-col-{column_sort_type}",
        violin_iqr=show_interquartile_range,
    )
    return summary(
        df,
        split_by=split_by,
        metric=metric,
        summary_type="violin",
        chart_params=chart_params,
        return_view=return_view,
        **kwargs,
    )


def summary_chart_functions() -> Dict[str, Callable]:
    return {
        "boxplot": boxplot,
        "bignumber": bignumber,
        "dimension_matrix": dimension_matrix,
        "heatmap": heatmap,
        "hexbin": hexbin,
        "histogram": histogram,
        "horizon": horizon,
        "ridgeline": ridgeline,
        "violin": violin,
    }
