import pandas as pd

from dx.formatters.main import handle_format
from dx.plotting.dex import basic
from dx.settings import get_settings

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
        view_metadata = basic.bar(df, return_view=True, **kwargs)
    elif kind == "line":
        view_metadata = basic.line(df, return_view=True, **kwargs)
    elif kind == "pie":
        view_metadata = basic.pie(df, return_view=True, **kwargs)
    elif kind == "scatter":
        view_metadata = basic.scatterplot(df, return_view=True, **kwargs)
    elif kind == "tilemap":
        view_metadata = basic.tilemap(df, return_view=True, **kwargs)
    elif kind == "violin":
        view_metadata = basic.violin(df, return_view=True, **kwargs)
    elif kind == "wordcloud":
        view_metadata = basic.wordcloud(df, return_view=True, **kwargs)
    else:
        raise NotImplementedError(f"{kind=} not yet supported for plotting.backend='dx'")

    handle_format(df, extra_metadata=view_metadata)
