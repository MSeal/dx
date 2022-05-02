import pandas as pd
from IPython import get_ipython
from IPython.core.formatters import BaseFormatter, DisplayFormatter
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


class DXBaseFormatter(BaseFormatter):
    print_method = "_repr_data_resource_"
    _return_type = (dict,)


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


def deregister(
    display_formatter: Optional[DisplayFormatter] = None,
) -> DisplayFormatter:
    """Reverts IPython.display_formatter to its original state"""
    if not IN_IPYTHON_ENV and display_formatter is None:
        return
    pd.options.display.max_rows = 60
    display_formatter.formatters.pop(DX_MEDIA_TYPE, None)
    return display_formatter


def register(display_formatter: Optional[DisplayFormatter] = None) -> DisplayFormatter:
    """Overrides the default IPython display formatter to use DXDisplayFormatter"""
    if not IN_IPYTHON_ENV and display_formatter is None:
        return
    pd.options.display.max_rows = 100_000

    display_formatter = display_formatter or get_ipython().display_formatter
    display_formatter.formatters[DX_MEDIA_TYPE] = DXBaseFormatter()
    display_formatter.formatters[DX_MEDIA_TYPE].for_type(pd.DataFrame, format_dx)
    return display_formatter


disable = deregister
enable = register
