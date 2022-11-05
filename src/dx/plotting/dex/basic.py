from typing import List, Optional, Union

import pandas as pd
import structlog
from pydantic import parse_obj_as

from dx.formatters.main import handle_format
from dx.types.charts._base import chart_view
from dx.types.charts._configs import (
    DEXBoundingType,
    DEXCombinationMode,
    DEXFormulaDisplay,
    DEXLineSmoothing,
    DEXLineType,
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
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXBarChartView]:
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

    if return_view:
        return view_metadata
    handle_format(df, extra_metadata=view_metadata)


def line(
    df,
    x: str,
    y: Union[List[str], str],
    line_type: Optional[DEXLineType] = "line",
    split_by: Optional[str] = None,
    multi_axis: Optional[bool] = False,
    smoothing: Optional[DEXLineSmoothing] = "none",
    use_count: bool = False,
    bounding_type: Optional[DEXBoundingType] = "absolute",
    zero_base_line: Optional[bool] = False,
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXLineChartView]:
    """
    Generates a DEX line plot from the given DataFrame.

    Params
    ------
    df: pd.DataFrame
        The DataFrame to plot.
    x: str
        The column to use for the x-axis.
    y: Union[List[str], str]
        The column(s) to use for the y-axis.
    line_type: Optional[DEXLineType]
        The line type to use:
            - bumparea
            - cumulative
            - line (default)
            - linepercent
            - stackedarea
            - stackedpercent
    split_by: Optional[str]
        The column to use for splitting the lines.
    multi_axis: Optional[bool]
        Whether to use multiple y-axes. (default: False)
    smoothing: Optional[DEXLineSmoothing]
        The line smoothing to use:
            - none (default)
            - hourly
            - daily
            - weekly
            - seven_day_moving_average
            - monthly
    use_count: bool
        Whether to use the DEX_COUNT column for the y-axis. (default: False)
    bounding_type: Optional[DEXBoundingType]
        The bounding type to use:
            - absolute (default)
            - relative
    zero_base_line: Optional[bool]
        Whether to use a zero base line. (default: False)

    **kwargs
        Additional keyword arguments to pass to the metadata update.
    """
    if str(x) not in df.columns:
        raise ValueError(f"Column '{x}' not found in DataFrame.")

    if isinstance(y, str):
        y = [y]
    for y_col in y:
        if str(y_col) not in df.columns:
            raise ValueError(f"Column '{y_col}' not found in DataFrame.")
    if use_count:
        y.append("DEX_COUNT")

    if split_by is not None:
        if str(split_by) not in df.columns:
            raise ValueError(f"Column '{split_by}' not found in DataFrame.")

    chart_settings = {
        "bounding_type": bounding_type,
        "line_smoothing": smoothing,
        "line_type": line_type,
        "multi_axis_line": multi_axis,
        "selected_metrics": y,
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

    if return_view:
        return view_metadata
    handle_format(df, extra_metadata=view_metadata)


def pie(
    df,
    x: str,
    y: str,
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXPieChartView]:
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

    # if return_view:
    #     return view_metadata
    # handle_format(df, extra_metadata=view_metadata)


def scatterplot(
    df: pd.DataFrame,
    x: str,
    y: str,
    trend_line: Optional[DEXTrendlineType] = None,
    size: Optional[str] = None,
    marginal_graphics: Optional[DEXSummaryType] = None,
    formula_display: Optional[DEXFormulaDisplay] = None,
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXScatterChartView]:
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

    if return_view:
        return view_metadata
    handle_format(df, extra_metadata=view_metadata)


def tilemap(
    df,
    lat: str,
    lon: str,
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXTilemapChartView]:
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

    # if return_view:
    #     return view_metadata
    # handle_format(df, extra_metadata=view_metadata)


def violin(
    df: pd.DataFrame,
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXViolinChartView]:
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

    # if return_view:
    #     return view_metadata
    # handle_format(df, extra_metadata=view_metadata)


def wordcloud(
    df: pd.DataFrame,
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXWordcloudChartView]:
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

    # if return_view:
    #     return view_metadata
    # handle_format(df, extra_metadata=view_metadata)
