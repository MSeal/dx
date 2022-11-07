import pandas as pd
import structlog
from pydantic import parse_obj_as

from dx.formatters.main import handle_format
from dx.plotting.dex import basic
from dx.settings import get_settings
from dx.types.charts._base import chart_view_ref

logger = structlog.get_logger(__name__)

settings = get_settings()


def enable_plotting_backend():
    """
    Enables the plotting backend for pandas.
    """
    global settings
    settings.PLOTTING_MODE = "dex"
    pd.options.plotting.backend = "dx"


def disable_plotting_backend():
    """
    Disables the plotting backend for pandas.
    """
    global settings
    settings.PLOTTING_MODE = "matplotlib"
    pd.options.plotting.backend = "matplotlib"


def plot(df: dict, kind: str, **kwargs) -> None:

    if kind == "bar":
        view = basic.bar(df, return_view=True, **kwargs)
    elif kind == "line":
        view = basic.line(df, return_view=True, **kwargs)
    elif kind == "pie":
        view = basic.pie(df, return_view=True, **kwargs)
    elif kind == "scatter":
        view = basic.scatterplot(df, return_view=True, **kwargs)
    elif kind == "tilemap":
        view = basic.tilemap(df, return_view=True, **kwargs)
    elif kind == "violin":
        view = basic.violin(df, return_view=True, **kwargs)
    elif kind == "wordcloud":
        view = basic.wordcloud(df, return_view=True, **kwargs)
    else:
        raise NotImplementedError(f"{kind=} not yet supported for plotting.backend='dx'")

    view_metadata = view.dict(exclude_unset=True)
    handle_format(df, extra_metadata=view_metadata)


def handle_view(
    df: pd.DataFrame,
    chart: dict,
    chart_mode: str,
    return_view: bool = False,
    **kwargs,
):
    """
    Converts a chart dictionary to a DEXChartView-inherited object
    and either passes it to be handled by the display formatter,
    or returns the view.
    """
    logger.info(f"{chart=}")

    view = parse_obj_as(
        chart_view_ref(),
        {
            "chart_mode": chart_mode,
            "chart": chart,
            **kwargs,
        },
    )
    view_metadata = view.dict(
        exclude_unset=True,
        exclude_none=True,
        by_alias=True,
    )
    logger.info(f"{view_metadata=}")

    if return_view:
        return view_metadata
    handle_format(df, extra_metadata=view_metadata)
