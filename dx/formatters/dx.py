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


class DXSettings(BaseSettings):
    DX_DISPLAY_MAX_ROWS: int = 100_000
    DX_DISPLAY_MAX_COLUMNS: int = 50
    DX_HTML_TABLE_SCHEMA: bool = Field(True, allow_mutation=False)
    DX_MEDIA_TYPE: str = Field("application/vnd.dex.v1+json", allow_mutation=False)
    DX_RENDERABLE_OBJECTS: List[type] = [pd.DataFrame, np.ndarray]

    class Config:
        validate_assignment = True  # we need this to enforce `allow_mutation`


@lru_cache
def get_dx_settings():
    return DXSettings()


dx_settings = get_dx_settings()


class DXDisplayFormatter(DisplayFormatter):
    def format(self, obj, **kwargs):

        if isinstance(obj, tuple(settings.RENDERABLE_OBJECTS)):
            display_id = str(uuid.uuid4())
            df_obj = pd.DataFrame(obj)
            payload, metadata = _render_dx(df_obj, display_id)
            # TODO: determine if/how we can pass payload/metadata with
            # display_id for the frontend to pick up properly
            return ({}, {})

        return DEFAULT_IPYTHON_DISPLAY_FORMATTER.format(obj, **kwargs)


def format_dx(df: pd.DataFrame, display_id: str) -> tuple:
    """
    Transforms the dataframe to a payload dictionary containing the
    table schema and column values as arrays.
    """
    # temporary workaround for numeric column rendering errors
    # https://noteables.slack.com/archives/C03CB8A4Z2L/p1658497348488939
    display_df = df.copy()
    display_df = stringify_columns(display_df)

    # temporary workaround for numeric MultiIndices
    # because of pandas build_table_schema() errors
    if isinstance(display_df.index, pd.MultiIndex):
        display_df = stringify_indices(display_df)

    # this will include the `df.index` by default (e.g. slicing/sampling)
    body = {
        "schema": build_table_schema(display_df),
        "data": display_df.reset_index().transpose().values.tolist(),
        "datalink": {},
    }
    if display_id is not None:
        body["datalink"]["display_id"] = display_id
    payload = {dx_settings.DX_MEDIA_TYPE: body}
    metadata = {dx_settings.DX_MEDIA_TYPE: {"display_id": display_id}}
    return (payload, metadata)


def _render_dx(df, display_id) -> tuple:
    df = truncate_if_too_big(df)
    payload, metadata = format_dx(df, display_id)
    # don't pass a dataframe in here, otherwise you'll get recursion errors
    with pd.option_context("html.table_schema", dx_settings.DX_HTML_TABLE_SCHEMA):
        ipydisplay(payload, raw=True, display_id=display_id)
    return (payload, metadata)


def register(ipython_shell: Optional[InteractiveShell] = None) -> None:
    """
    Enables the DEX media type output display formatting and
    updates global dx & pandas settings with DX settings.
    """
    if not IN_IPYTHON_ENV and ipython_shell is None:
        return

    global settings
    settings.DISPLAY_MODE = "enhanced"

    settings.DISPLAY_MAX_COLUMNS = dx_settings.DX_DISPLAY_MAX_COLUMNS
    settings.DISPLAY_MAX_ROWS = dx_settings.DX_DISPLAY_MAX_ROWS
    settings.MEDIA_TYPE = dx_settings.DX_MEDIA_TYPE
    settings.RENDERABLE_OBJECTS = dx_settings.DX_RENDERABLE_OBJECTS

    pd.set_option("display.max_columns", dx_settings.DX_DISPLAY_MAX_COLUMNS)
    pd.set_option("display.max_rows", dx_settings.DX_DISPLAY_MAX_ROWS)

    ipython = ipython_shell or get_ipython()
    ipython.display_formatter = DXDisplayFormatter()
