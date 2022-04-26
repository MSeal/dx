import pandas as pd
from IPython import get_ipython
from IPython.core.formatters import DisplayFormatter
from pandas.io.json import build_table_schema

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


def deregister() -> None:
    """Reverts IPython.display_formatter to its original state"""
    pd.options.display.max_rows = 60
    get_ipython().display_formatter = DEFAULT_IPYTHON_DISPLAY_FORMATTER


def register() -> None:
    """Overrides the default IPython display formatter to use DXDisplayFormatter"""
    pd.options.display.max_rows = 100_000
    get_ipython().display_formatter = DXDisplayFormatter()


disable = deregister
enable = register
