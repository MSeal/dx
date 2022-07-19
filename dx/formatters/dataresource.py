import uuid
from typing import Optional

import pandas as pd
from IPython import get_ipython
from IPython.core.formatters import DisplayFormatter
from IPython.core.interactiveshell import InteractiveShell
from IPython.display import display as ipydisplay
from pandas.io.json import build_table_schema

from dx.config import DEFAULT_IPYTHON_DISPLAY_FORMATTER, IN_IPYTHON_ENV
from dx.formatters.types import DATARESOURCE_MEDIA_TYPE
from dx.formatters.utils import truncate_if_too_big

DATARESOURCE_DISPLAY_MAX_ROWS = 100_000
DATARESOURCE_HTML_TABLE_SCHEMA = True


class DXDataResourceDisplayFormatter(DisplayFormatter):
    def format(self, obj, **kwargs):

        if isinstance(obj, pd.DataFrame):
            display_id = str(uuid.uuid4())
            payload, metadata = _render_dataresource(obj, display_id)
            # TODO: determine if/how we can pass payload/metadata with
            # display_id for the frontend to pick up properly
            return ({}, {})

        return DEFAULT_IPYTHON_DISPLAY_FORMATTER.format(obj, **kwargs)


def format_dataresource(df: pd.DataFrame, display_id: str) -> tuple:
    """
    Transforms the dataframe to a payload dictionary containing the
    table schema and column values as arrays.
    """
    body = {
        "schema": build_table_schema(df),
        "data": df.reset_index().to_dict("records"),
        "datalink": {},
    }
    if display_id is not None:
        body["datalink"]["display_id"] = display_id
    payload = {DATARESOURCE_MEDIA_TYPE: body}
    metadata = {DATARESOURCE_MEDIA_TYPE: {"display_id": display_id}}
    return (payload, metadata)


def _render_dataresource(df, display_id) -> tuple:
    df = truncate_if_too_big(df)
    payload, metadata = format_dataresource(df, display_id)
    # don't pass a dataframe in here, otherwise you'll get recursion errors
    with pd.option_context("html.table_schema", True):
        ipydisplay(payload, raw=True, display_id=display_id)
    return (payload, metadata)


def deregister(ipython_shell: Optional[InteractiveShell] = None) -> None:
    """
    Disables the DEX display formatting configuration with
    the table schema supported DataResource media type.
    """
    if not IN_IPYTHON_ENV and ipython_shell is None:
        return
    pd.set_option("html.table_schema", DATARESOURCE_HTML_TABLE_SCHEMA)
    pd.options.display.max_rows = DATARESOURCE_DISPLAY_MAX_ROWS
    ipython = ipython_shell or get_ipython()
    ipython.display_formatter = DXDataResourceDisplayFormatter()
