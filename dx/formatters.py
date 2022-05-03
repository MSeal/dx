import pandas as pd
from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell
from IPython.core.formatters import DisplayFormatter
from pandas.io.json import build_table_schema
from typing import Optional

IN_IPYTHON_ENV = get_ipython() is not None

DEFAULT_IPYTHON_DISPLAY_FORMATTER = None
if IN_IPYTHON_ENV:
    DEFAULT_IPYTHON_DISPLAY_FORMATTER = get_ipython().display_formatter

DX_MEDIA_TYPE = "application/vnd.dex.v1+json"


class DXDisplayFormatter(DisplayFormatter):
    def format(self, obj, **kwargs):

        if isinstance(obj, pd.DataFrame):
            return format_dx(obj)

        return DEFAULT_IPYTHON_DISPLAY_FORMATTER.format(obj, **kwargs)


def format_dx(df) -> tuple:
    """
    Transforms the dataframe to a payload dictionary containing the table schema
    and column values as arrays.
    """
    # this will include the `df.index` by default (e.g. slicing/sampling)
    payload = {
        DX_MEDIA_TYPE: {
            "schema": build_table_schema(df),
            "data": df.reset_index().transpose().values.tolist(),
        }
    }
    metadata = {}
    return (payload, metadata)


def deregister(ipython_shell: Optional[InteractiveShell] = None) -> None:
    """Reverts IPython.display_formatter to its original state"""
    if not IN_IPYTHON_ENV and ipython_shell is None:
        return
    pd.options.display.max_rows = 60
    ipython = ipython_shell or get_ipython()
    ipython.display_formatter = DEFAULT_IPYTHON_DISPLAY_FORMATTER


def register(ipython_shell: Optional[InteractiveShell] = None) -> None:
    """Overrides the default IPython display formatter to use DXDisplayFormatter"""
    if not IN_IPYTHON_ENV and ipython_shell is None:
        return
    pd.options.display.max_rows = 100_000

    if ipython_shell is not None:
        global DEFAULT_IPYTHON_DISPLAY_FORMATTER
        DEFAULT_IPYTHON_DISPLAY_FORMATTER = ipython_shell.display_formatter

    ipython = ipython_shell or get_ipython()
    ipython.display_formatter = DXDisplayFormatter()


disable = deregister
enable = register
