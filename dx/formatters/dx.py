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
from dx.loggers import get_logger
from dx.sampling import sample_and_describe
from dx.settings import settings
from dx.utils import df_is_subset, get_applied_filters, get_display_id, normalize_index_and_columns


class DXSettings(BaseSettings):
    DX_DISPLAY_MAX_ROWS: int = 100_000
    DX_DISPLAY_MAX_COLUMNS: int = 50
    DX_HTML_TABLE_SCHEMA: bool = Field(True, allow_mutation=False)
    DX_MEDIA_TYPE: str = Field("application/vnd.dex.v1+json", allow_mutation=False)
    DX_RENDERABLE_OBJECTS: List[type] = [pd.DataFrame, np.ndarray]

    class Config:
        validate_assignment = True  # we need this to enforce `allow_mutation`
        json_encoders = {type: lambda t: str(t)}


@lru_cache
def get_dx_settings():
    return DXSettings()


dx_settings = get_dx_settings()

logger = get_logger(__name__)


class DXDisplayFormatter(DisplayFormatter):
    def format(self, obj, **kwargs):

        if isinstance(obj, tuple(settings.RENDERABLE_OBJECTS)):
            update_existing_display = df_is_subset(obj)
            applied_filters = get_applied_filters(obj)
            display_id = get_display_id(obj)
            format_dx(
                obj,
                display_id=display_id,
                update=update_existing_display,
                filters=applied_filters,
            )
            return ({}, {})

        return DEFAULT_IPYTHON_DISPLAY_FORMATTER.format(obj, **kwargs)


def generate_dx_body(
    df: pd.DataFrame,
    display_id: Optional[str] = None,
    filters: Optional[list[dict]] = None,
) -> tuple:
    """
    Transforms the dataframe to a payload dictionary containing the
    table schema and column values as arrays.
    """
    # this will include the `df.index` by default (e.g. slicing/sampling)
    payload_body = {
        "schema": build_table_schema(df),
        "data": df.reset_index().transpose().values.tolist(),
        "datalink": {},
    }
    payload = {dx_settings.DX_MEDIA_TYPE: payload_body}

    metadata_body = {
        "datalink": {
            "dataframe_info": {},
            "dx_settings": settings.json(exclude={"RENDERABLE_OBJECTS": True}),
            "applied_filters": filters,
        },
    }
    metadata = {dx_settings.DX_MEDIA_TYPE: metadata_body}

    display_id = display_id or str(uuid.uuid4())
    payload_body["datalink"]["display_id"] = display_id
    metadata_body["datalink"]["display_id"] = display_id

    return (payload, metadata)


def format_dx(df: pd.DataFrame, display_id: Optional[str] = None) -> tuple:
    df = normalize_index_and_columns(df)
    df, dataframe_info = sample_and_describe(df)
    payload, metadata = generate_dx_body(df, display_id)
    metadata[dx_settings.DX_MEDIA_TYPE]["datalink"]["dataframe_info"] = dataframe_info

    # don't pass a dataframe in here, otherwise you'll get recursion errors
    with pd.option_context("html.table_schema", dx_settings.DX_HTML_TABLE_SCHEMA):
        ipydisplay(payload, raw=True, metadata=metadata, display_id=display_id)

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
