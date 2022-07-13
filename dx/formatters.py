import uuid
import warnings
from typing import Optional

import pandas as pd
from IPython import get_ipython
from IPython.core.formatters import DisplayFormatter
from IPython.core.interactiveshell import InteractiveShell
from IPython.display import display as ipydisplay
from pandas.io.json import build_table_schema

warnings.filterwarnings("ignore")

IN_IPYTHON_ENV = get_ipython() is not None

DEFAULT_IPYTHON_DISPLAY_FORMATTER = None
if IN_IPYTHON_ENV:
    DEFAULT_IPYTHON_DISPLAY_FORMATTER = get_ipython().display_formatter


DATARESOURCE_MEDIA_TYPE = "application/vnd.dataresource+json"
DX_MEDIA_TYPE = "application/vnd.dex.v1+json"

DISPLAY_ID_TO_DATAFRAME = {}


class DXDisplayFormatter(DisplayFormatter):
    def format(self, obj, **kwargs):

        if isinstance(obj, pd.DataFrame):
            display_id = _register_df_display_id(obj)
            _, metadata = _render_dx(obj, display_id)
            return ({}, {})

        return DEFAULT_IPYTHON_DISPLAY_FORMATTER.format(obj, **kwargs)


class DXDataResourceDisplayFormatter(DisplayFormatter):
    def format(self, obj, **kwargs):

        if isinstance(obj, pd.DataFrame):
            display_id = _register_df_display_id(obj)
            _, metadata = _render_dataresource(obj, display_id)
            return ({}, {})

        return DEFAULT_IPYTHON_DISPLAY_FORMATTER.format(obj, **kwargs)


def format_dx(df: pd.DataFrame, display_id: str) -> tuple:
    """
    Transforms the dataframe to a payload dictionary containing the
    table schema and column values as arrays.
    """
    # this will include the `df.index` by default (e.g. slicing/sampling)
    payload = {
        DX_MEDIA_TYPE: {
            "schema": build_table_schema(df),
            "data": df.reset_index().transpose().values.tolist(),
            "datalink": {
                "display_id": display_id,
            },
        }
    }
    metadata = {DX_MEDIA_TYPE: {"display_id": display_id}}
    return (payload, metadata)


def format_dataresource(df: pd.DataFrame, display_id: str) -> tuple:
    """
    Transforms the dataframe to a payload dictionary containing the
    table schema and column values as arrays.
    """
    payload = {
        DATARESOURCE_MEDIA_TYPE: {
            "schema": build_table_schema(df),
            "data": df.reset_index().to_dict("records"),
            "datalink": {
                "display_id": display_id,
            },
        }
    }
    metadata = {DATARESOURCE_MEDIA_TYPE: {"display_id": display_id}}
    return (payload, metadata)


def deregister(ipython_shell: Optional[InteractiveShell] = None) -> None:
    """
    Disables the DEX display formatting configuration with
    the table schema supported DataResource media type."""
    if not IN_IPYTHON_ENV and ipython_shell is None:
        return
    pd.set_option("html.table_schema", False)
    pd.options.display.max_rows = 100_000
    ipython = ipython_shell or get_ipython()
    ipython.display_formatter = DXDataResourceDisplayFormatter()


def register(ipython_shell: Optional[InteractiveShell] = None) -> None:
    """
    Enables the DEX media type output display formatting.
    """
    if not IN_IPYTHON_ENV and ipython_shell is None:
        return
    pd.set_option("html.table_schema", False)
    pd.options.display.max_rows = 100_000
    ipython = ipython_shell or get_ipython()
    ipython.display_formatter = DXDisplayFormatter()


def reset(ipython_shell: Optional[InteractiveShell] = None) -> None:
    """
    Resets all nteract/Noteable options,
    reverting to the default pandas display options.
    """
    if not IN_IPYTHON_ENV and ipython_shell is None:
        return
    pd.set_option("html.table_schema", False)
    pd.options.display.max_rows = 60
    ipython = ipython_shell or get_ipython()
    ipython.display_formatter = DEFAULT_IPYTHON_DISPLAY_FORMATTER


def _register_df_display_id(df):
    global DISPLAY_ID_TO_DATAFRAME

    # don't keep track of a dataframe rendered multiple times?
    # dataframe_to_display_id = {
    #     str(dataframe): display_id
    #     for display_id, dataframe in DISPLAY_ID_TO_DATAFRAME.items()
    # }
    # if existing_display_id := dataframe_to_display_id.get(str(df)):
    #     DISPLAY_ID_TO_DATAFRAME.pop(existing_display_id, None)

    display_id = str(uuid.uuid4())
    DISPLAY_ID_TO_DATAFRAME[display_id] = df
    return display_id


def _render_dataresource(df, display_id) -> tuple:
    payload, metadata = format_dataresource(df, display_id)
    # don't pass a dataframe in here, otherwise you'll get recursion errors
    with pd.option_context("html.table_schema", True):
        ipydisplay(payload, raw=True, display_id=display_id)
    return (payload, metadata)


def _render_dx(df, display_id) -> tuple:
    payload, metadata = format_dx(df, display_id)
    # don't pass a dataframe in here, otherwise you'll get recursion errors
    with pd.option_context("html.table_schema", True):
        ipydisplay(payload, raw=True, display_id=display_id)
    return (payload, metadata)


disable = deregister
enable = register
