from typing import List, Optional, Union

import structlog

from dx.plotting.utils import handle_view, raise_for_missing_columns
from dx.types.charts import options
from dx.types.charts.connected_scatter import DEXConnectedScatterChartView
from dx.types.charts.correlation_matrix import DEXCorrelationMatrixChartView
from dx.types.charts.diverging_bar import DEXDivergingBarChartView
from dx.types.charts.dotplot import DEXDotPlotChartView
from dx.types.charts.parcoords import DEXParallelCoordinatesChartView
from dx.types.charts.radar_plot import DEXRadarPlotChartView
from dx.types.charts.scatterplot_matrix import DEXScatterPlotMatrixChartView

logger = structlog.get_logger()

__all__ = [
    "connected_scatterplot",
    "correlation_matrix",
    "diverging_bar",
    "dotplot",
    "parallel_coordinates",
    "radar_plot",
    "scatterplot_matrix",
]


def sample_connected_scatterplot(df, **kwargs) -> Optional[DEXConnectedScatterChartView]:
    return handle_view(df, chart_mode="connected_scatter", **kwargs)


def connected_scatterplot(df, **kwargs) -> Optional[DEXConnectedScatterChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_connected_scatterplot(df, **kwargs)


def sample_correlation_matrix(df, **kwargs) -> Optional[DEXCorrelationMatrixChartView]:
    return handle_view(df, chart_mode="correlation_matrix", **kwargs)


def correlation_matrix(df, **kwargs) -> Optional[DEXCorrelationMatrixChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_correlation_matrix(df, **kwargs)


def sample_diverging_bar(df, **kwargs) -> Optional[DEXDivergingBarChartView]:
    return handle_view(df, chart_mode="diverging_bar", **kwargs)


def diverging_bar(df, **kwargs) -> Optional[DEXDivergingBarChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_diverging_bar(df, **kwargs)


def sample_dotplot(df, **kwargs) -> Optional[DEXDotPlotChartView]:
    return handle_view(df, chart_mode="dotplot", **kwargs)


def dotplot(df, **kwargs) -> Optional[DEXDotPlotChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_dotplot(df, **kwargs)


def sample_radar_plot(df, **kwargs) -> Optional[DEXRadarPlotChartView]:
    return handle_view(df, chart_mode="dotplot", chart={"bar_projection": "radial"}, **kwargs)


def radar_plot(df, **kwargs) -> Optional[DEXRadarPlotChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_radar_plot(df, **kwargs)


def sample_parallel_coordinates(df, **kwargs) -> Optional[DEXParallelCoordinatesChartView]:
    return handle_view(df, chart_mode="parcoords", **kwargs)


def parallel_coordinates(
    df,
    columns: Union[List[str], str],
    filtered_only: options.DEXParCoordsShowData = False,
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
    return_view: bool
        Whether to return a `DEXView` object instead of render.
    **kwargs
        Additional keyword arguments to pass to the view metadata.
    """

    if isinstance(columns, str):
        columns = [columns]
    raise_for_missing_columns(columns, df.columns)

    chart_settings = {
        "filtered_data_only": filtered_only,
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


# aliasing for easy reference
parcoords = parallel_coordinates


def sample_scatterplot_matrix(df, **kwargs) -> Optional[DEXScatterPlotMatrixChartView]:
    return handle_view(df, chart_mode="scatterplot_matrix", **kwargs)


def scatterplot_matrix(df, **kwargs) -> Optional[DEXScatterPlotMatrixChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_scatterplot_matrix(df, **kwargs)
