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
        "summary_type": "ridgeline",
        "summary_bins": bins,
        "sort_columns_by": f"{sort_order}-col-{column_sort_type}",
    }

    return handle_view(
        df,
        chart_mode="summary",
        chart=chart_settings,
        return_view=return_view,
        **kwargs,
    )

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
        "summary_type": "histogram",
        "summary_bins": bins,
        "sort_columns_by": f"{sort_order}-col-{column_sort_type}",
    }

    return handle_view(
        df,
        chart_mode="summary",
        chart=chart_settings,
        return_view=return_view,
        **kwargs,
    )

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
        "summary_type": "heatmap",
        "summary_bins": bins,
        "sort_columns_by": f"{sort_order}-col-{column_sort_type}",
    }

    return handle_view(
        df,
        chart_mode="summary",
        chart=chart_settings,
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
        "summary_type": "horizon",
        "summary_bins": bins,
        "sort_columns_by": f"{sort_order}-col-{column_sort_type}",
    }

    return handle_view(
        df,
        chart_mode="summary",
        chart=chart_settings,
        return_view=return_view,
        **kwargs,
    )

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
        Whether boxplot whiskers go to min/max or to 1.5x interquartile range with outliers beyond that range shown individually
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
        "summary_type": "boxplot",
        "sort_columns_by": f"{sort_order}-col-{column_sort_type}",
    }

    return handle_view(
        df,
        chart_mode="summary",
        chart=chart_settings,
        return_view=return_view,
        **kwargs,
    )

def bignumber(
    df: pd.DataFrame,
    split_by: str,
    metric: str,
    second_metric: str = "none",
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
    show_outliers: bool
        Whether boxplot whiskers go to min/max or to 1.5x interquartile range with outliers beyond that range shown individually
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
        "summary_type": "boxplot",
        "sort_columns_by": f"{sort_order}-col-{column_sort_type}",
    }

    return handle_view(
        df,
        chart_mode="summary",
        chart=chart_settings,
        return_view=return_view,
        **kwargs,
    )

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