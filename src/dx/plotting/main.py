from typing import List

import pandas as pd
import structlog
from pydantic import parse_obj_as

from dx.formatters.main import handle_format
from dx.plotting.dex import _samples, basic
from dx.settings import get_settings, settings_context
from dx.types.charts._base import chart_view_ref

logger = structlog.get_logger(__name__)

settings = get_settings()


def enable_plotting_backend():
    """
    Convenience toggle for enabling the dx plotting backend for pandas.
    """
    pd.options.plotting.backend = "dx"


def disable_plotting_backend():
    """
    Convenience toggle for disabling the dx plotting backend for pandas and reverting to matplotlib.
    """
    pd.options.plotting.backend = "matplotlib"


def plot(df: dict, kind: str, **kwargs) -> None:
    # ref: https://github.com/plotly/plotly.py/blob/master/packages/python/plotly/plotly/__init__.py
    if kind == "bar":
        view = basic.bar(df, return_view=True, **kwargs)
    elif kind == "line":
        view = basic.line(df, return_view=True, **kwargs)
    elif kind == "pie":
        view = basic.pie(df, return_view=True, **kwargs)
    elif kind == "scatter":
        view = basic.scatter(df, return_view=True, **kwargs)
    elif kind == "tilemap":
        view = basic.tilemap(df, return_view=True, **kwargs)
    elif kind == "violin":
        view = basic.violin(df, return_view=True, **kwargs)
    elif kind == "wordcloud":
        view = basic.wordcloud(df, return_view=True, **kwargs)
    elif (sample_chart := getattr(_samples, f"sample_{kind}", None)) is not None:
        view = sample_chart(df, return_view=True, **kwargs)
    elif kind == "dashboard":
        from dx.plotting.dashboards import dashboard

        return dashboard(df, **kwargs)
    else:
        raise NotImplementedError(f"{kind=} not yet supported for plotting.backend='dx'")

    view_metadata = view.dict(
        exclude_unset=True,
        exclude_none=True,
        by_alias=True,
    )
    logger.debug(f"{view_metadata=}")

    with settings_context(generate_dex_metadata=True):
        # if someone is calling one of these functions with the dx plotting backend,
        # there isn't any way around persisting frontend-generated metadata,
        # so anything existing will be replaced with the new metadata here
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
    logger.debug(f"{chart=}")

    view_params = {
        "chart_mode": chart_mode,
        "chart": chart,
        "decoration": {"title": f"📊 dx {chart_mode}"},
    }
    view_params.update(kwargs)

    view = parse_obj_as(
        chart_view_ref(),
        view_params,
    )
    if return_view:
        return view

    view_metadata = view.dict(
        exclude_unset=True,
        exclude_none=True,
        by_alias=True,
    )
    logger.debug(f"{view_metadata=}")
    with settings_context(generate_dex_metadata=True):
        handle_format(df, extra_metadata=view_metadata)


def raise_for_missing_columns(columns: List[str], existing_columns: pd.Index) -> None:
    """
    Checks if a column exists in a dataframe or is "index".
    If both fail, this raises a ValueError.
    """
    if isinstance(columns, str):
        columns = [columns]

    for column in columns:
        if str(column) == "index":
            return
        if column in existing_columns:
            return
        raise ValueError(f"Column `{column}` not found in DataFrame")
