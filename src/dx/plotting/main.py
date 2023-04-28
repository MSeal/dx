import pandas as pd
import structlog

from dx.formatters.main import handle_format
from dx.plotting import dex
from dx.plotting.dashboards import dashboard
from dx.settings import get_settings, settings_context

logger = structlog.get_logger(__name__)

settings = get_settings()

__all__ = [
    "enable_plotting_backend",
    "disable_plotting_backend",
    "plot",
]


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
    view = dex.get_chart_view(df, kind, **kwargs)
    if view:
        pass
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
