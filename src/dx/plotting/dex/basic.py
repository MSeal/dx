from typing import List, Optional, Union

import pandas as pd
import structlog
from pydantic.color import Color

from dx.plotting.main import handle_view
from dx.types.charts._configs import (
    DEXBoundingType,
    DEXCombinationMode,
    DEXFormulaDisplay,
    DEXLineSmoothing,
    DEXLineType,
    DEXPieLabelContents,
    DEXPieLabelType,
    DEXProBarModeType,
    DEXSortColumnsBy,
    DEXSummaryType,
    DEXTextDataFormat,
    DEXTrendlineType,
    DEXWordRotate,
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
    sort_columns_by: Optional[DEXSortColumnsBy] = "asc-col-string",
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
    if str(x) != "index" and str(x) not in df.columns:
        raise ValueError(f"Column '{x}' not found in DataFrame.")
    if str(y) != "index" and str(y) not in df.columns:
        raise ValueError(f"Column '{y}' not found in DataFrame.")

    chart_settings = {
        "dim1": x,
        "metric1": y,
        "bar_projection": "horizontal" if horizontal else "vertical",
        "sort_columns_by": sort_columns_by,
        "group_other": group_other,
        "combination_mode": str(combination_mode).upper(),
    }
    if bar_width is not None:
        chart_settings["metric3"] = bar_width
    if y2 is not None:
        chart_settings["second_bar_metric"] = y2
        chart_settings["pro_bar_mode"] = str(pro_bar_mode).title()

    return handle_view(
        df,
        chart_mode="bar",
        chart=chart_settings,
        return_view=return_view,
        **kwargs,
    )


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
    zero_baseline: Optional[bool] = False,
    return_view: bool = False,
    combination_mode: Optional[DEXCombinationMode] = "avg",
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
    zero_baseline: Optional[bool]
        Whether to use a zero base line. (default: False)
    combination_mode: Optional[DEXCombinationMode]
        The combination mode to use (avg, sum, min, median, max, or count).

    **kwargs
        Additional keyword arguments to pass to the metadata update.
    """
    if str(x) != "index" and str(x) not in df.columns:
        raise ValueError(f"Column '{x}' not found in DataFrame.")

    if isinstance(y, str):
        y = [y]
    for y_col in y:
        if str(y_col) != "index" and str(y_col) not in df.columns:
            raise ValueError(f"Column '{y_col}' not found in DataFrame.")
    if use_count:
        y.append("DEX_COUNT")

    if split_by is not None:
        if str(split_by) not in df.columns:
            raise ValueError(f"Column '{split_by}' not found in DataFrame.")

    chart_settings = {
        "bounding_type": bounding_type,
        "combination_mode": str(combination_mode).upper(),
        "line_smoothing": smoothing,
        "line_type": line_type,
        "multi_axis_line": multi_axis,
        "selected_metrics": y,
        "split_lines_by": split_by,
        "timeseries_sort": x,
        "zero_baseline": zero_baseline,
    }
    logger.info(f"{chart_settings=}")
    return handle_view(
        df,
        chart_mode="line",
        chart=chart_settings,
        return_view=return_view,
        **kwargs,
    )


def pie(
    df,
    split_slices_by: str,
    slice_size: str,
    show_total: bool = True,
    pie_label_type: Optional[DEXPieLabelType] = "rim",
    pie_label_contents: Optional[DEXPieLabelContents] = "name",
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

    if str(split_slices_by) != "index" and str(split_slices_by) not in df.columns:
        raise ValueError(f"Column '{split_slices_by}' not found in DataFrame.")
    if str(split_slices_by) != "index" and str(slice_size) not in df.columns:
        raise ValueError(f"Column '{slice_size}' not found in DataFrame.")

    chart_settings = {
        "dim1": split_slices_by,
        "metric1": slice_size,
        "show_total": show_total,
        "pie_label_type": pie_label_type,
        "pie_label_contents": pie_label_contents,
    }
    return handle_view(
        df,
        chart_mode="pie",
        chart=chart_settings,
        return_view=return_view,
        **kwargs,
    )


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
    if str(x) != "index" and str(x) not in df.columns:
        raise ValueError(f"Column '{x}' not found in DataFrame.")
    if str(y) != "index" and str(y) not in df.columns:
        raise ValueError(f"Column '{y}' not found in DataFrame.")

    chart_settings = {
        "metric1": x,
        "metric2": y,
    }
    # if these are present but set to `None`, DEX gets angry
    if trend_line is not None:
        chart_settings["trendLine"] = trend_line
    if size is not None:
        chart_settings["scatterplotSize"] = size
    if marginal_graphics is not None:
        chart_settings["marginalGraphics"] = marginal_graphics
    if formula_display is not None:
        chart_settings["formulaDisplay"] = formula_display

    return handle_view(
        df,
        chart_mode="scatter",
        chart=chart_settings,
        return_view=return_view,
        **kwargs,
    )


def tilemap(
    df,
    lat: str,
    lon: str,
    icon_fill_color: Color = "#000000",
    icon_opacity: float = 1.0,
    icon_size: int = 2,
    icon_type: str = "point",
    stroke_color: Color = "#000000",
    stroke_width: int = 2,
    map_mode: str = "tile",
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXTilemapChartView]:
    """
    Generates a DEX tilemap from the given DataFrame.

    Params
    ------
    df: pd.DataFrame
        The DataFrame to plot.
    lat: str
        The column to use for the latitude.
    lon: str
        The column to use for the longitude.
    icon_fill_color: Color
        The color to use for the icon fill.
    icon_opacity: float
        The opacity to use for the icon (0.0 to 1.0).
    icon_size: int
        The size to use for the icon. (0 to 10; default: 2)
    icon_type: str
        The type of icon to use. One of "point", "circle", "square", "diamond", "triangle", "star", "cross", or "x".
    stroke_color: Color
        The color to use for the icon stroke.
    stroke_width: int
        The width to use for the icon stroke.
    map_mode: str
        The type of map to use. One of "tile" or "satellite".

    **kwargs
        Additional keyword arguments to pass to the plot view.
    """
    if str(lat) != "index" and str(lat) not in df.columns:
        raise ValueError(f"Column '{lat}' not found in DataFrame.")
    if str(lon) != "index" and str(lon) not in df.columns:
        raise ValueError(f"Column '{lon}' not found in DataFrame.")

    layer_settings = {
        "lat_dim": lat,
        "long_dim": lon,
        "color": icon_fill_color,
        "transparency": icon_opacity,
        "size": icon_size,
        "type": icon_type,
        "stroke": stroke_color,
        "stroke_width": stroke_width,
        # "hover_opts": {},
        # "point_size_opts": {}
    }
    chart_settings = {
        "map_mode": map_mode,
        "layer_settings": [layer_settings],
    }
    return handle_view(
        df,
        chart_mode="tilemap",
        chart=chart_settings,
        return_view=return_view,
        **kwargs,
    )


def violin(
    df: pd.DataFrame,
    x: str,
    y: str,
    bin_count: int = 30,
    show_interquartile_range: bool = False,
    horizontal: bool = False,
    sort_columns_by: Optional[DEXSortColumnsBy] = "asc-col-string",
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXViolinChartView]:
    """
    Generates a DEX violin plot from the given DataFrame.

    Params
    ------
    df: pd.DataFrame
        The DataFrame to plot.
    x: str
        The column to use for the x-axis.
    y: str
        The column to use for the y-axis.
    bin_count: int
        The number of bins to use for the violin plot.
    show_interquartile_range: bool
        Whether to show the interquartile range.
    horizontal: bool
        Whether to plot the violin horizontally. (default: False)
    sort_columns_by: Optional[DEXSortColumnsBy]
        The method to use for sorting columns. One of "asc-col-string", "desc-col-string", "asc-col-number", "desc-col-number", "asc-col-date",
        or "desc-col-date".

    **kwargs
        Additional keyword arguments to pass to the plot view.
    """
    if str(x) != "index" and str(x) not in df.columns:
        raise ValueError(f"Column '{x}' not found in DataFrame.")
    if str(y) != "index" and str(y) not in df.columns:
        raise ValueError(f"Column '{y}' not found in DataFrame.")

    chart_settings = {
        "dim1": x,
        "metric1": y,
        "horizontal": "horizontal" if horizontal else "vertical",
        "summary_type": "violin",
        "summary_bins": bin_count,
        "violin_iqr": show_interquartile_range,
        "sort_columns_by": sort_columns_by,
    }

    return handle_view(
        df,
        chart_mode="violin",
        chart=chart_settings,
        return_view=return_view,
        **kwargs,
    )


def wordcloud(
    df: pd.DataFrame,
    word_column: str,
    size_column: str,
    text_format: Optional[DEXTextDataFormat] = "sentence",
    word_rotation: Optional[DEXWordRotate] = None,
    random_coloring: bool = False,
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXWordcloudChartView]:
    """
    Generates a DEX wordcloud from the given DataFrame.

    Params
    ------
    df: pd.DataFrame
        The DataFrame to plot.
    word_column: str
        The column to use for the words in the cloud.
    size_column: str
        The column to use for the size of the words in the cloud.
    text_format: Optional[DEXTextDataFormat]
        The format of the text data. Either "sentence" or "token".
    word_rotation: Optional[DEXWordRotate]
        The rotation to use for the words in the cloud (45, 90, "jitter", or None).
    random_coloring: bool
        Whether to use random coloring for the words in the cloud.

    **kwargs
        Additional keyword arguments to pass to the plot view.
    """
    if str(word_column) != "index" and str(word_column) not in df.columns:
        raise ValueError(f"Column '{word_column}' not found in DataFrame.")
    if str(size_column) != "index" and str(size_column) not in df.columns:
        raise ValueError(f"Column '{size_column}' not found in DataFrame.")

    chart_settings = {
        "text_data_format": text_format,
        "token_metric": size_column,
        "word_data": word_column,
        "word_color": "random" if random_coloring else "none",
        "word_rotate": word_rotation if word_rotation else "none",
    }
    return handle_view(
        df,
        chart_mode="wordcloud",
        chart=chart_settings,
        return_view=return_view,
        **kwargs,
    )
