from typing import List, Optional, Union

import pandas as pd
import structlog
from pydantic.color import Color

from dx.plotting.main import handle_view, raise_for_missing_columns
from dx.types.charts import options
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
    y2_style: options.DEXSecondMetricstyle = "bar",
    horizontal: bool = False,
    bar_width: Optional[str] = None,
    group_other: bool = False,
    column_sort_order: options.DEXSortColumnsByOrder = "asc",
    column_sort_type: options.DEXSortColumnsByType = "string",
    pro_bar_mode: options.DEXProBarModeType = "combined",
    combination_mode: options.DEXCombinationMode = "avg",
    show_bar_labels: bool = False,
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXBarChartView]:
    """
    Generates a DEX bar plot from the given DataFrame.

    Parameters
    ----------
    df: pd.DataFrame
        The DataFrame to plot.
    x: str
        The column to use for the x-axis.
    y: List[str]
        The column(s) to use for the primary y-axis.
    y2: Optional[str]
        The column to use for the secondary y-axis.
    y2_style: DEXSecondMetricstyle
        The style to use for the secondary y-axis. (`"bar"` or `"dot"`)
    horizontal: bool
        Whether to plot the bars horizontally.
    bar_width: Optional[str]
        The column to use for the bar width.
    group_other: bool
        Whether to group the remaining columns into an "Other" category.
    column_sort_order: DEXSortColumnsByOrder
        The order to sort the columns by (`"asc"` or `"desc"`)
    column_sort_type: DEXSortColumnsByType
        The type of sorting to use. (`"number"`, `"string"`, or `"date"`)
    pro_bar_mode: DEXProBarModeType
        The bar mode to use (`"clustered"`, `"combined"`, or `"stacked"`).
    combination_mode: DEXCombinationMode
        The combination mode to use (`"avg"`, `"sum"`, `"min"`, `"median"`, `"max"`, or `"count"`).
    show_bar_labels: bool
        Whether to show the bar values as labels.
    return_view: bool
        Whether to return a `DEXView` object instead of render.
    **kwargs
        Additional keyword arguments to pass to the view metadata.
    """
    raise_for_missing_columns(x, df.columns)

    if not isinstance(y, list):
        y = [y]
    raise_for_missing_columns(y, df.columns)
    y1 = y[0]

    chart_settings = {
        "dim1": x,
        "metric1": y1,
        "bar_projection": "horizontal" if horizontal else "vertical",
        "sort_columns_by": f"{column_sort_order}-col-{column_sort_type}",
        "group_other": group_other,
        "combination_mode": combination_mode,
        "bar_label": "show" if show_bar_labels else "none",
        "selected_bar_metrics": y,
    }
    if bar_width is not None:
        chart_settings["metric3"] = bar_width
    if y2 is not None:
        chart_settings["second_bar_metric"] = y2
        chart_settings["pro_bar_mode"] = pro_bar_mode
        chart_settings["second_metric_style"] = y2_style

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
    line_type: options.DEXLineType = "line",
    split_by: Optional[str] = None,
    multi_axis: bool = False,
    smoothing: Optional[options.DEXLineSmoothing] = None,
    use_count: bool = False,
    bounding_type: options.DEXBoundingType = "absolute",
    zero_baseline: bool = False,
    combination_mode: options.DEXCombinationMode = "avg",
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXLineChartView]:
    """
    Generates a DEX line plot from the given DataFrame.

    Parameters
    ----------
    df: pd.DataFrame
        The DataFrame to plot.
    x: str
        The column to use for the x-axis.
    y: Union[List[str], str]
        The column(s) to use for the y-axis.
    line_type: DEXLineType
        The line type to use:
            - `"bumparea"`
            - `"cumulative"`
            - `"line"` (default)
            - `"linepercent"`
            - `"stackedarea"`
            - `"stackedpercent"`
    split_by: Optional[str]
        The column to use for splitting the lines.
    multi_axis: bool
        Whether to use multiple y-axes.
    smoothing: Optional[DEXLineSmoothing]
        The line smoothing to use:
            - `None` (default)
            - `"hourly"`
            - `"daily"`
            - `"weekly"`
            - `"seven_day_moving_average"`
            - `"monthly"`
    use_count: bool
        Whether to use the DEX_COUNT column for the y-axis.
    bounding_type: DEXBoundingType
        The bounding type to use:
            - `"absolute"` (default)
            - `"relative"`
    zero_baseline: bool
        Whether to use a zero base line.
    combination_mode: DEXCombinationMode
        The combination mode to use (`"avg"`, `"sum"`, `"min"`, `"median"`, `"max"`, or `"count"`).
    return_view: bool
        Whether to return a `DEXView` object instead of render.
    **kwargs
        Additional keyword arguments to pass to the view metadata.
    """
    raise_for_missing_columns(x, df.columns)

    if isinstance(y, str):
        y = [y]
    raise_for_missing_columns(y, df.columns)
    if use_count:
        y.append("DEX_COUNT")

    if split_by is not None:
        if str(split_by) not in df.columns:
            raise ValueError(f"Column '{split_by}' not found in DataFrame.")

    chart_settings = {
        "bounding_type": bounding_type,
        "combination_mode": combination_mode,
        "line_smoothing": smoothing or "none",
        "line_type": line_type,
        "multi_axis_line": multi_axis,
        "selected_metrics": y,
        "split_lines_by": split_by,
        "timeseries_sort": x,
        "zero_baseline": zero_baseline,
    }
    logger.debug(f"{chart_settings=}")
    return handle_view(
        df,
        chart_mode="line",
        chart=chart_settings,
        return_view=return_view,
        **kwargs,
    )


def pie(
    df,
    y: str,
    split_slices_by: Optional[str] = None,
    show_total: bool = True,
    pie_label_type: options.DEXPieLabelType = "rim",
    pie_label_contents: options.DEXPieLabelContents = "name",
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXPieChartView]:
    """
    Generates a DEX pie plot from the given DataFrame.

    Parameters
    ----------
    df: pd.DataFrame
        The DataFrame to plot.
    y: str
        The column to use for the slice size.
    split_slices_by: Optional[str]
        The column to use for splitting the slices. If not provided, slices will be split and sized by `y`.
    show_total: bool
        Whether to show the total.
    pie_label_type: DEXPieLabelType
        The pie label type to use:
            - `"rim"` (default)
            - `"annotation"`
            - `"center"`
            - `"stem"`
            - `"none"`
    pie_label_contents: DEXPieLabelContents
        The pie label contents to use:
            - `"name"` (default)
            - `"value"`
            - `"percent"`
            - `"name_value"`
            - `"name_percent"`
            - `"value_percent"`
    return_view: bool
        Whether to return a `DEXView` object instead of render.
    **kwargs
        Additional keyword arguments to pass to the view metadata.
    """
    if split_slices_by is None:
        split_slices_by = y
    raise_for_missing_columns([y, split_slices_by], df.columns)

    chart_settings = {
        "dim1": split_slices_by,
        "metric1": y,
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


def scatter(
    df: pd.DataFrame,
    x: str,
    y: str,
    size: Optional[str] = None,
    trend_line: Optional[options.DEXTrendlineType] = None,
    marginal_graphics: Optional[options.DEXSummaryType] = None,
    formula_display: Optional[options.DEXFormulaDisplay] = None,
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXScatterChartView]:
    """
    Generates a DEX scatterplot from the given DataFrame.

    Parameters
    ----------
    df: pd.DataFrame
        The DataFrame to plot.
    x: str
        The column to use for the x-axis.
    y: str
        The column to use for the y-axis.
    size: Optional[str]
        The column to use for sizing scatterplot points.
    trend_line: Optional[DEXTrendlineType]
        The type of trendline to use. One of `"linear"`, `"exponential"`, `"polynomial"`, `"power"`, or `"logarithmic"`.
    marginal_graphics: Optional[DEXSummaryType]
        The marginal graphics to use:
            - `boxplot`
            - `heatmap`
            - `histogram`
            - `horizon`
            - `joy`
            - `ridgeline`
            - `violin`
    formula_display: Optional[DEXFormulaDisplay]
        The formula display to use:
            - `r2`
            - `formula`
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
    icon_opacity: float = 1.0,
    icon_size: int = 2,
    icon_size_scale: options.DEXScale = "linear",
    stroke_color: Color = "#000000",
    stroke_width: int = 2,
    label_column: Optional[str] = None,
    tile_layer: str = "streets",
    hover_cols: Optional[List[str]] = None,
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXTilemapChartView]:
    """
    Generates a DEX tilemap from the given DataFrame.

    Parameters
    ----------
    df: pd.DataFrame
        The DataFrame to plot.
    lat: str
        The column to use for the latitude values.
    lon: str
        The column to use for the longitude values.
    icon_opacity: float
        The opacity to use for the icon (`0.0` to `1.0`)
    icon_size: Union[int, str]
        Either:
        - int: a fixed size to use for the icon (`0` to `10`)
        - str: a column name to use for functional sizing
    icon_size_scale: DEXScale
        The scale to use for functional sizing (`"linear"` or `"log"`)
    stroke_color: Color
        The color to use for the icon stroke.
    stroke_width: int
        The width to use for the icon stroke.
    tile_layer: str
        The type of tile layer to use. One of `"streets"`, `"outdoors"`, `"light"`, `"dark"`, or `"satellite"`
    return_view: bool
        Whether to return a `DEXView` object instead of render.
    **kwargs
        Additional keyword arguments to pass to the view metadata.
    """
    raise_for_missing_columns([lat, lon], df.columns)

    if isinstance(hover_cols, str):
        hover_cols = [hover_cols]
    if hover_cols is None:
        hover_cols = df.columns
    else:
        raise_for_missing_columns(hover_cols, df.columns)

    if label_column is not None:
        raise_for_missing_columns(label_column, df.columns)

    if isinstance(icon_size, str):
        # referencing a column, treat as functional sizing

        if icon_size not in df.columns:
            # "index" was chosen but isn't in columns, which passes raise_for_missing_columns()
            series = df.index
        else:
            series = df[icon_size]

        series_min = series.min()
        if str(icon_size_scale).lower() == "log":
            series_min = 1

        point_size_opts = {
            "mode": "functional",
            "size": 2,
            "met": icon_size,
            "scale": icon_size_scale,
            "min": series_min,
            "max": series.max(),
            "sizeMin": 1,
            "sizeMax": 10,
        }
    elif isinstance(icon_size, int):
        # fixed sizing, shouldn't matter what we put in here
        point_size_opts = {
            "mode": "fixed",
            "size": icon_size,
            "met": str(lon),
            "scale": icon_size_scale,
            "min": df[str(lon)].min(),
            "max": df[str(lon)].max(),
            "sizeMin": 1,
            "sizeMax": 10,
        }
    else:
        raise ValueError(f"`{type(icon_size)}` is not a valid type for `icon_size`.")

    # determine which columns are numeric and which ones are strings/mixed/etc
    dimension_cols = [col for col in hover_cols if df[col].dtype == "object"]
    metric_cols = [col for col in hover_cols if col not in dimension_cols]

    layer_settings = {
        "lat_dim": lat,
        "long_dim": lon,
        "transparency": icon_opacity,
        "size": icon_size,
        "type": "point",
        "stroke": stroke_color,
        "stroke_width": stroke_width,
        "point_size_opts": point_size_opts,
        "hover_opts": {
            "dims": dimension_cols,
            "mets": metric_cols,
        },
        "tile_layer": tile_layer,
    }
    if label_column is not None:
        layer_settings["show_labels"] = label_column

    chart_settings = {
        "map_mode": "tile",
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
    raise_for_missing_columns([split_by, metric], df.columns)

    # this is weird because the default is "desc" even though the values
    # in DEX look like they go in ascending order from top->bottom in
    # the horizontal view. if that changes, this will need to be removed/updated
    if str(column_sort_order).lower() == "asc":
        sort_order = "desc"
    elif str(column_sort_order).lower() == "desc":
        sort_order = "asc"

    chart_settings = {
        "dim1": split_by,
        "metric1": metric,
        "summary_type": "violin",
        "summary_bins": bins,
        "violin_iqr": show_interquartile_range,
        "sort_columns_by": f"{sort_order}-col-{column_sort_type}",
    }

    return handle_view(
        df,
        chart_mode="summary",
        chart=chart_settings,
        return_view=return_view,
        **kwargs,
    )


def wordcloud(
    df: pd.DataFrame,
    word_column: str,
    size: str,
    text_format: options.DEXTextDataFormat = "sentence",
    word_rotation: Optional[options.DEXWordRotate] = None,
    random_coloring: bool = False,
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXWordcloudChartView]:
    """
    Generates a DEX wordcloud from the given DataFrame.

    Parameters
    ----------
    df: pd.DataFrame
        The DataFrame to plot.
    word_column: str
        The column to use for the words in the cloud.
    size: str
        The column to use for the size of the words in the cloud.
    text_format: DEXTextDataFormat
        The format of the text data. Either `"sentence"` or `"token"`.
    word_rotation: Optional[DEXWordRotate]
        The rotation to use for the words in the cloud (`45`, `90`, `"jitter"`, or `None`).
    random_coloring: bool
        Whether to use random coloring for the words in the cloud.
    return_view: bool
        Whether to return a `DEXView` object instead of render.
    **kwargs
        Additional keyword arguments to pass to the view metadata.
    """
    raise_for_missing_columns([word_column, size], df.columns)

    chart_settings = {
        "text_data_format": text_format,
        "token_metric": size,
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
