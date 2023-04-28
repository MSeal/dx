from typing import List, Optional, Union

import pandas as pd
import structlog

from dx.plotting.dex.summary import summary
from dx.plotting.utils import handle_view, raise_for_missing_columns
from dx.types.charts import options
from dx.types.charts.bar import DEXBarChartView
from dx.types.charts.dataprism import DEXDataPrismChartView
from dx.types.charts.line import DEXLineChartView
from dx.types.charts.pie import DEXPieChartView
from dx.types.charts.scatter import DEXScatterChartView
from dx.types.charts.summary import DEXSummaryChartView, DEXViolinChartView
from dx.types.charts.wordcloud import DEXWordcloudChartView

logger = structlog.get_logger(__name__)

__all__ = [
    "bar",
    "dataprism",
    "line",
    "pie",
    "scatter",
    "violin",
    "wordcloud",
]


def sample_bar(df, **kwargs) -> Optional[DEXBarChartView]:
    return handle_view(df, chart_mode="bar", **kwargs)


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


def sample_line(df, **kwargs) -> Optional[DEXLineChartView]:
    return handle_view(df, chart_mode="line", **kwargs)


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


def sample_pie(df, **kwargs) -> Optional[DEXPieChartView]:
    return handle_view(df, chart_mode="pie", **kwargs)


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


def sample_scatter(df, **kwargs) -> Optional[DEXScatterChartView]:
    return handle_view(df, chart_mode="scatter", **kwargs)


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


def sample_wordcloud(df, **kwargs) -> Optional[DEXWordcloudChartView]:
    return handle_view(df, chart_mode="wordcloud", **kwargs)


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


def sample_dataprism(df, **kwargs) -> Optional[DEXDataPrismChartView]:
    return handle_view(df, chart_mode="dataprism", **kwargs)


def dataprism(
    df: pd.DataFrame,
    suggestion_fields: Optional[List[str]] = None,
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXDataPrismChartView]:
    """
    Generates an automatic Data Prism for the given dataframe. In the future, we can run a
    prioritized Data Prism if the user sends fields.

    Parameters
    ----------
    suggestion_fields: Optional[List[str]]
        The fields to use for the Data Prism. If empty, it will work on the entire table in fully
        automatic mode. If not empty, it will use the fields for Prioritized mode.
    df: pd.DataFrame
        The DataFrame to plot.
    return_view: bool
        Whether to return a `DEXView` object instead of render.
    **kwargs
        Additional keyword arguments to pass to the view metadata.
    """
    suggestion_fields = suggestion_fields or []
    if suggestion_fields:
        raise_for_missing_columns(suggestion_fields, df.columns)

    # decorated_suggestion_fields is a transformation of suggestion fields into 'FIELDNAME - Metric|Dimension'. Metric if are number, int or datetime, Dimension otherwise
    decorated_suggestion_fields = []
    for column in df.columns:
        if column not in suggestion_fields:
            continue
        # mixed dtypes or string -> dim
        if df[column].dtype == "object":
            decorated_suggestion_fields.append(f"{column} - Dimension")
            continue
        # bool dtype -> dim
        if df[column].dtype == "bool":
            decorated_suggestion_fields.append(f"{column} - Dimension")
            continue
        # numeric, datetime -> metric
        decorated_suggestion_fields.append(f"{column} - Metric")

    chart_settings = {
        "suggestion_fields": decorated_suggestion_fields,
    }
    return handle_view(
        df,
        chart_mode="dataprism",
        chart=chart_settings,
        return_view=return_view,
        **kwargs,
    )
