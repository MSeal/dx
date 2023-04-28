import pandas as pd
import structlog

from dx.formatters.main import handle_format
from dx.plotting import dex
from dx.plotting.dashboards import dashboard
from dx.settings import get_settings, settings_context

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
    """Main plotting backend for dx. `kind` must be passed through to determine the appropriate
    chart type ("line" by default).

    ref: https://github.com/plotly/plotly.py/blob/master/packages/python/plotly/plotly/__init__.py
    """
    view = None

    # main chart categories
    chart_modules = [
        dex.basic,
        dex.comparison,
        dex.funnel,
        dex.maps,
        dex.part_to_whole,
        dex.summary,
        dex.time_series,
    ]
    for chart_module in chart_modules:
        if chart_func := getattr(chart_module, kind, None):
            view = chart_func(df, return_view=True, **kwargs)
            break

    if view:
        pass
    # direct chart passthrough with no configs
    elif (sample_chart_func := getattr(dex._samples, f"sample_{kind}", None)) is not None:
        view = sample_chart_func(df, return_view=True, **kwargs)
    elif kind == "dashboard":
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
