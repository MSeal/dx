from typing import List, Optional, Union

import pandas as pd
import structlog
from pydantic import parse_obj_as

from dx.types.charts._base import chart_view
from dx.types.charts._configs import (
    DEXBoundingType,
    DEXCombinationMode,
    DEXFormulaDisplay,
    DEXLineSmoothing,
    DEXProBarModeType,
    DEXSortColumnsBy,
    DEXSummaryType,
    DEXTrendlineType,
)
from dx.types.charts.bar import DEXBarChartView
from dx.types.charts.line import DEXLineChartView
from dx.types.charts.pie import DEXPieChartView
from dx.types.charts.scatter import DEXScatterChartView
from dx.types.charts.tilemap import DEXTilemapChartView
from dx.types.charts.violin import DEXViolinChartView
from dx.types.charts.wordcloud import DEXWordcloudChartView

logger = structlog.get_logger(__name__)


def bar(
    df,
    x: str,
    y: str,
    y2: Optional[str] = None,
    horizontal: bool = False,
    bar_width: Optional[str] = None,
    group_other: Optional[bool] = False,
    sort_columns_by: Optional[DEXSortColumnsBy] = "asc_col_string",
    pro_bar_mode: Optional[DEXProBarModeType] = "combined",
    combination_mode: Optional[DEXCombinationMode] = "avg",
    **kwargs,
) -> DEXBarChartView:
    """
    Generates a DEX bar plot from the given DataFrame.

    Params
    ------
    df: pd.DataFrame
        The DataFrame to plot.
    x: str
        The column to use for the x-axis.
    y: str
        The column to use for the y-axis.
    y2: Optional[str]
        The column to use for the secondary y-axis.
    horizontal: bool
        Whether to plot the bars horizontally.
    bar_width: Optional[str]
        The column to use for the bar width.
    group_other: bool
        Whether to group the remaining columns into an "Other" category.
    sort_columns_by: Optional[DEXSortColumnsBy]
        How to sort the columns.
    pro_bar_mode: Optional[DEXProBarModeType]
        The bar mode to use (clustered, combined, or stacked).
    combination_mode: Optional[DEXCombinationMode]
        The combination mode to use (avg, sum, min, median, max, or count).

    **kwargs
        Additional keyword arguments to pass to the metadata update.
    """
    if str(x) not in df.columns:
        raise ValueError(f"Column '{x}' not found in DataFrame.")
    if str(y) not in df.columns:
        raise ValueError(f"Column '{y}' not found in DataFrame.")

    chart_settings = {
        "dim1": x,
        "metric1": y,
        "bar_projection": "horizontal" if horizontal else "vertical",
        "sort_columns_by": sort_columns_by,
        "group_other": group_other,
        "combination_mode": combination_mode,
    }
    if bar_width is not None:
        chart_settings["metric3"] = bar_width
    if y2 is not None:
        chart_settings["second_bar_metric"] = y2
        chart_settings["pro_bar_mode"] = pro_bar_mode

    view_metadata = parse_obj_as(
        chart_view(),
        {
            "chart_mode": "bar",
            "chart": chart_settings,
            **kwargs,
        },
    )
    logger.info(f"{view_metadata=}")

    return view_metadata


def line(
    df,
    x: str,
    y_columns: Union[List[str], str],
    use_count: bool = False,
    split_by: Optional[str] = None,
    multi_axis: Optional[bool] = False,
    bounding_type: Optional[DEXBoundingType] = "absolute",
    smoothing: Optional[DEXLineSmoothing] = "none",
    zero_base_line: Optional[bool] = False,
    **kwargs,
) -> DEXLineChartView:
    """
    Generates a DEX line plot from the given DataFrame.

    Params
    ------
    df: pd.DataFrame
        The DataFrame to plot.
    x: str
        The column to use for the x-axis.
    y_columns: Union[List[str], str]
        The column(s) to use for the y-axis.
    split_by: Optional[str]
        The column to use for plotting multiple lines.
    bounding_type: Optional[DEXBoundingType]
        The bounding type to use (absolute or relative).
    smoothing: Optional[str]


    **kwargs
        Additional keyword arguments to pass to the metadata update.
    """
    if str(x) not in df.columns:
        raise ValueError(f"Column '{x}' not found in DataFrame.")

    if isinstance(y_columns, str):
        y_columns = [y_columns]
    for y_col in y_columns:
        if str(y_col) not in df.columns:
            raise ValueError(f"Column '{y_col}' not found in DataFrame.")
    if use_count:
        y_columns.append("DEX_COUNT")

    if split_by is not None:
        if str(split_by) not in df.columns:
            raise ValueError(f"Column '{split_by}' not found in DataFrame.")

    chart_settings = {
        "bounding_type": bounding_type,
        "line_smoothing": smoothing,
        "line_type": "line",
        "multi_axis_line": multi_axis,
        "selected_metrics": y_columns,
        "split_lines_by": split_by,
        "timeseries_sort": x,
        "zero_base_line": zero_base_line,
    }
    logger.info(f"{chart_settings=}")

    view_metadata = parse_obj_as(
        chart_view(),
        {
            "chart_mode": "line",
            "chart": chart_settings,
            **kwargs,
        },
    )
    logger.info(f"{view_metadata=}")

    return view_metadata


def pie(df, x: str, y: str, **kwargs) -> DEXPieChartView:
    """
    Generates a DEX pie plot from the given DataFrame.

    Params
    ------
    df: pd.DataFrame
        The DataFrame to plot.

    **kwargs
        Additional keyword arguments to pass to the plot view.
    """
    raise NotImplementedError("Pie plots are not yet supported.")


def scatterplot(
    df: pd.DataFrame,
    x: str,
    y: str,
    trend_line: Optional[DEXTrendlineType] = None,
    size: Optional[str] = None,
    marginal_graphics: Optional[DEXSummaryType] = None,
    formula_display: Optional[DEXFormulaDisplay] = None,
    **kwargs,
) -> DEXScatterChartView:
    """
    Generates a DEX scatterplot from the given DataFrame.

    Params
    ------
    df: pd.DataFrame
        The DataFrame to plot.
    x: str
        The column to use for the x-axis.
    y: str
        The column to use for the y-axis.
    trendline: str
        The type of trendline to use. One of "linear", "exponential", "polynomial", "power", or "logarithmic".
    size: str
        The column to use for sizing scatterplot points.
    **kwargs
        Additional keyword arguments to pass to the metadata update.
    """
    if str(x) not in df.columns:
        raise ValueError(f"Column '{x}' not found in DataFrame.")
    if str(y) not in df.columns:
        raise ValueError(f"Column '{y}' not found in DataFrame.")

    chart_settings = {
        "metric1": x,
        "metric2": y,
    }
    # if these are present but set to `None`, DEX gets angry
    if trend_line is not None:
        chart_settings["chart"]["trendLine"] = trend_line
    if size is not None:
        chart_settings["chart"]["scatterplotSize"] = size
    if marginal_graphics is not None:
        chart_settings["chart"]["marginalGraphics"] = marginal_graphics
    if formula_display is not None:
        chart_settings["chart"]["formulaDisplay"] = formula_display

    logger.info(f"{chart_settings=}")

    view_metadata = parse_obj_as(
        chart_view(),
        {
            "chart_mode": "scatter",
            "chart": chart_settings,
            **kwargs,
        },
    )
    logger.info(f"{view_metadata=}")

    return view_metadata


def tilemap(df, lat: str, lon: str, **kwargs) -> DEXTilemapChartView:
    """
    Generates a DEX tilemap from the given DataFrame.

    Params
    ------
    df: pd.DataFrame
        The DataFrame to plot.

    **kwargs
        Additional keyword arguments to pass to the plot view.
    """
    raise NotImplementedError("Tilemaps are not yet supported.")


def violin(df: pd.DataFrame) -> DEXViolinChartView:
    """
    Generates a DEX violin plot from the given DataFrame.

    Params
    ------
    df: pd.DataFrame
        The DataFrame to plot.

    **kwargs
        Additional keyword arguments to pass to the plot view.
    """
    raise NotImplementedError("Violin plots are not yet supported.")


def wordcloud(df: pd.DataFrame) -> DEXWordcloudChartView:
    """
    Generates a DEX wordcloud from the given DataFrame.

    Params
    ------
    df: pd.DataFrame
        The DataFrame to plot.

    **kwargs
        Additional keyword arguments to pass to the plot view.
    """
    raise NotImplementedError("Wordclouds are not yet supported.")
