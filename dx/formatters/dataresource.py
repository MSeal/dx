import uuid
from functools import lru_cache
from typing import List, Optional

import numpy as np
import pandas as pd
from IPython import get_ipython
from IPython.core.formatters import DisplayFormatter
from IPython.core.interactiveshell import InteractiveShell
from IPython.display import display as ipydisplay
from pandas.io.json import build_table_schema
from pydantic import BaseSettings, Field

from dx.config import DEFAULT_IPYTHON_DISPLAY_FORMATTER, IN_IPYTHON_ENV
from dx.formatters.utils import (
    stringify_columns,
    stringify_indices,
    truncate_if_too_big,
)
from dx.settings import settings


class DataResourceSettings(BaseSettings):
    # "simple" (classic simpleTable/DEX) display mode
    DATARESOURCE_DISPLAY_MAX_ROWS: int = 100_000
    DATARESOURCE_DISPLAY_MAX_COLUMNS: int = 50
    DATARESOURCE_HTML_TABLE_SCHEMA: bool = Field(True, allow_mutation=False)
    DATARESOURCE_MEDIA_TYPE: str = Field(
        "application/vnd.dataresource+json", allow_mutation=False
    )
    DATARESOURCE_RENDERABLE_OBJECTS: List[type] = [pd.DataFrame, np.ndarray]

    class Config:
        validate_assignment = True  # we need this to enforce `allow_mutation`


@lru_cache
def get_dataresource_settings():
    return DataResourceSettings()


dataresource_settings = get_dataresource_settings()


class DXDataResourceDisplayFormatter(DisplayFormatter):
    def format(self, obj, **kwargs):

        if isinstance(obj, tuple(settings.RENDERABLE_OBJECTS)):
            display_id = str(uuid.uuid4())
            df_obj = pd.DataFrame(obj)
            payload, metadata = _render_dataresource(df_obj, display_id)
            # TODO: determine if/how we can pass payload/metadata with
            # display_id for the frontend to pick up properly
            return ({}, {})

        return DEFAULT_IPYTHON_DISPLAY_FORMATTER.format(obj, **kwargs)


def format_dataresource(df: pd.DataFrame, display_id: str) -> tuple:
    """
    Transforms the dataframe to a payload dictionary containing the
    table schema and column values as arrays.
    """
    # temporary workaround for numeric column rendering errors with GRID
    # https://noteables.slack.com/archives/C03CB8A4Z2L/p1658497348488939
    display_df = df.copy()
    display_df = stringify_columns(display_df)

    # temporary workaround for numeric MultiIndices
    # because of pandas build_table_schema() errors
    if isinstance(display_df.index, pd.MultiIndex):
        display_df = stringify_indices(display_df)

    body = {
        "schema": build_table_schema(display_df),
        "data": display_df.reset_index().to_dict("records"),
        "datalink": {},
    }
    if display_id is not None:
        body["datalink"]["display_id"] = display_id
    payload = {dataresource_settings.DATARESOURCE_MEDIA_TYPE: body}
    metadata = {
        dataresource_settings.DATARESOURCE_MEDIA_TYPE: {"display_id": display_id}
    }
    return (payload, metadata)


def _render_dataresource(df, display_id) -> tuple:
    df = truncate_if_too_big(df)
    payload, metadata = format_dataresource(df, display_id)
    # don't pass a dataframe in here, otherwise you'll get recursion errors
    with pd.option_context(
        "html.table_schema", dataresource_settings.DATARESOURCE_HTML_TABLE_SCHEMA
    ):
        ipydisplay(payload, raw=True, display_id=display_id)
    return (payload, metadata)


def deregister(ipython_shell: Optional[InteractiveShell] = None) -> None:
    """
    Sets the current IPython display formatter as the dataresource
    display formatter, used for simpleTable / "classic DEX" outputs
    and updates global dx & pandas settings with dataresource settings.
    """
    if not IN_IPYTHON_ENV and ipython_shell is None:
        return

    global settings
    settings.DISPLAY_MODE = "simple"

    settings.DISPLAY_MAX_COLUMNS = (
        dataresource_settings.DATARESOURCE_DISPLAY_MAX_COLUMNS
    )
    settings.DISPLAY_MAX_ROWS = dataresource_settings.DATARESOURCE_DISPLAY_MAX_ROWS
    settings.MEDIA_TYPE = dataresource_settings.DATARESOURCE_MEDIA_TYPE
    settings.RENDERABLE_OBJECTS = dataresource_settings.DATARESOURCE_RENDERABLE_OBJECTS

    pd.set_option(
        "display.max_columns", dataresource_settings.DATARESOURCE_DISPLAY_MAX_COLUMNS
    )
    pd.set_option(
        "display.max_rows", dataresource_settings.DATARESOURCE_DISPLAY_MAX_ROWS
    )

    ipython = ipython_shell or get_ipython()
    ipython.display_formatter = DXDataResourceDisplayFormatter()
