from typing import Optional

import pandas as pd

from dx.formatters.main import handle_format
from dx.settings import get_settings
from dx.types.dex_plotting import DEXFormulaDisplay, DEXSummaryType, DEXTrendlineType

settings = get_settings()


DEFAULT_PANDAS_SCATTERPLOT = pd.DataFrame.plot.scatter


def enable_plotting_backend():
    """
    Enables the plotting backend for pandas.
    """
    global settings
    settings.PLOTTING_MODE = "dex"
    pd.options.plotting.backend = "dx"
    # pd.DataFrame.plot.scatter = scatterplot


def disable_plotting_backend():
    """
    Disables the plotting backend for pandas.
    """
    global settings
    settings.PLOTTING_MODE = "matplotlib"
    pd.options.plotting.backend = "matplotlib"
    # pd.DataFrame.plot.scatter = DEFAULT_PANDAS_SCATTERPLOT


def scatterplot(
    df: pd.DataFrame,
    x: str,
    y: str,
    trend_line: Optional[DEXTrendlineType] = None,
    size: Optional[str] = None,
    marginal_graphics: Optional[DEXSummaryType] = None,
    formula_dislpay: Optional[DEXFormulaDisplay] = None,
    **kwargs,
) -> None:
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
    if str(x) not in df.columns:
        raise ValueError(f"Column '{x}' not found in DataFrame.")
    if str(y) not in df.columns:
        raise ValueError(f"Column '{y}' not found in DataFrame.")

    chart_metadata = {
        "chart": {
            "metric1": x,
            "metric2": y,
        },
        "chart_mode": "scatter",
        **kwargs,
    }

    # if these are present but set to `None`, DEX gets angry
    if trend_line is not None:
        chart_metadata["chart"]["trendLine"] = trend_line
    if size is not None:
        chart_metadata["chart"]["scatterplotSize"] = size
    if marginal_graphics is not None:
        chart_metadata["chart"]["marginalGraphics"] = marginal_graphics
    if formula_dislpay is not None:
        chart_metadata["chart"]["formulaDisplay"] = formula_dislpay

    handle_format(
        df,
        extra_metadata=chart_metadata,
    )


def plot(df: dict, kind: str, **kwargs):
    # https://github.com/plotly/plotly.py/blob/17b7c27f9e17b413b6958835ad53dc1aefb90834/doc/python/pandas-backend.md
    # https://github.com/plotly/plotly.py/blob/6018bffcc09d375846b6c72ab906e998b0dd71d6/packages/python/plotly/plotly/__init__.py

    if kind == "scatter":
        scatterplot(df, **kwargs)
        return

    raise NotImplementedError(f"{kind=} not yet supported for plotting.backend='dx'")
