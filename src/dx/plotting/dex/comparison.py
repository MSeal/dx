from typing import List, Optional, Union

import structlog

from dx.plotting.main import handle_view, raise_for_missing_columns
from dx.types.charts import options
from dx.types.charts.parcoords import DEXParallelCoordinatesChartView

__all__ = ["parcoords"]

logger = structlog.get_logger()


def parcoords(
    df,
    columns: Union[List[str], str],
    filtered_only: bool = False,
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXParallelCoordinatesChartView]:
    """
    Generates a DEX Parallel Coordinates view from the given DataFrame.

    Parameters
    ----------
    df: pd.DataFrame
        The DataFrame to plot.
    columns: Union[List[str], str]
        The columns plotted on the parallel coordinates, in the order displayed
    filtered_only: bool
        Whether to only show filtered data.
    return_view: bool
        Whether to return a `DEXView` object instead of render.
    **kwargs
        Additional keyword arguments to pass to the view metadata.
    """

    if isinstance(columns, str):
        columns = [columns]
    raise_for_missing_columns(columns, df.columns)

    # "All Data" or "Filtered Data Only"
    filter_value = options.DEXParCoordsShowData.false
    if filtered_only:
        filter_value = options.DEXParCoordsShowData.true

    chart_settings = {
        "filtered_data_only": filter_value,
        "parcoords_columns": columns,
    }
    logger.debug(f"{chart_settings=}")
    return handle_view(
        df,
        chart_mode="line",
        chart=chart_settings,
        return_view=return_view,
        **kwargs,
    )
