import uuid
from functools import lru_cache
from typing import Optional

import numpy as np
import pandas as pd
import structlog
from IPython import get_ipython
from IPython.core.formatters import DisplayFormatter
from IPython.core.interactiveshell import InteractiveShell
from IPython.display import display
from pandas.io.json import build_table_schema
from pydantic import BaseSettings, Field

from dx.formatters.main import DEFAULT_IPYTHON_DISPLAY_FORMATTER
from dx.sampling import get_df_dimensions, sample_if_too_big
from dx.settings import settings
from dx.utils.datatypes import to_dataframe
from dx.utils.formatting import generate_metadata, is_default_index, normalize_index_and_columns
from dx.utils.tracking import (
    DISPLAY_ID_TO_METADATA,
    DISPLAY_ID_TO_ORIG_COLUMN_DTYPES,
    SUBSET_TO_DATAFRAME_HASH,
    generate_df_hash,
    get_display_id,
    register_display_id,
    store_in_sqlite,
    track_column_conversions,
)


class DataResourceSettings(BaseSettings):
    # "simple" (classic simpleTable/DEX) display mode
    DATARESOURCE_DISPLAY_MAX_ROWS: int = 100_000
    DATARESOURCE_DISPLAY_MAX_COLUMNS: int = 50
    DATARESOURCE_HTML_TABLE_SCHEMA: bool = Field(True, allow_mutation=False)
    DATARESOURCE_MEDIA_TYPE: str = Field("application/vnd.dataresource+json", allow_mutation=False)

    DATARESOURCE_FLATTEN_INDEX_VALUES: bool = False
    DATARESOURCE_FLATTEN_COLUMN_VALUES: bool = True
    DATARESOURCE_STRINGIFY_INDEX_VALUES: bool = False
    DATARESOURCE_STRINGIFY_COLUMN_VALUES: bool = True

    class Config:
        validate_assignment = True  # we need this to enforce `allow_mutation`
        json_encoders = {type: lambda t: str(t)}


@lru_cache
def get_dataresource_settings():
    return DataResourceSettings()


dataresource_settings = get_dataresource_settings()

logger = structlog.get_logger(__name__)


def handle_dataresource_format(
    obj,
    ipython_shell: Optional[InteractiveShell] = None,
):
    ipython = ipython_shell or get_ipython()

    logger.debug(f"*** handling dataresource format for {type(obj)=} ***")
    if not isinstance(obj, pd.DataFrame):
        obj = to_dataframe(obj)
    logger.debug(f"{obj.shape=}")

    default_index_used = is_default_index(obj.index)

    if not settings.ENABLE_DATALINK:
        obj = normalize_index_and_columns(obj)
        payload, metadata = format_dataresource(
            obj,
            has_default_index=default_index_used,
        )
        return payload, metadata

    orig_obj = obj.copy()
    orig_dtypes = orig_obj.dtypes.to_dict()
    obj = normalize_index_and_columns(obj)
    obj_hash = generate_df_hash(obj)
    update_existing_display = obj_hash in SUBSET_TO_DATAFRAME_HASH
    display_id = get_display_id(obj_hash)

    # to be referenced during update_display_id() after
    # data is pulled from sqlite in order to put dtypes back
    # to their original states
    if display_id not in DISPLAY_ID_TO_ORIG_COLUMN_DTYPES:
        DISPLAY_ID_TO_ORIG_COLUMN_DTYPES[display_id] = orig_dtypes

    if not update_existing_display:
        sqlite_df_table = register_display_id(
            obj,
            display_id=display_id,
            df_hash=obj_hash,
            ipython_shell=ipython,
        )

    track_column_conversions(
        orig_df=orig_obj,
        df=obj,
        display_id=display_id,
    )
    del orig_obj

    payload, metadata = format_dataresource(
        obj,
        update=update_existing_display,
        display_id=display_id,
        has_default_index=default_index_used,
    )

    # this needs to happen after sending to the frontend
    # so the user doesn't wait as long for writing larger datasets
    if not update_existing_display:
        store_in_sqlite(sqlite_df_table, obj)

    return payload, metadata


class DXDataResourceDisplayFormatter(DisplayFormatter):
    formatters = DEFAULT_IPYTHON_DISPLAY_FORMATTER.formatters

    def format(self, obj, **kwargs):

        if isinstance(obj, tuple(settings.RENDERABLE_OBJECTS)):
            handle_dataresource_format(obj)
            return ({}, {})

        return DEFAULT_IPYTHON_DISPLAY_FORMATTER.format(obj, **kwargs)


def generate_dataresource_body(
    df: pd.DataFrame,
    display_id: Optional[str] = None,
) -> tuple:
    """
    Transforms the dataframe to a payload dictionary containing the
    table schema and column values as arrays.
    """
    schema = build_table_schema(df)
    logger.debug(f"{schema=}")

    # fillna(np.nan) to handle pd.NA values
    data = df.fillna(np.nan).reset_index().to_dict("records")

    payload = {
        "schema": schema,
        "data": data,
        "datalink": {"display_id": display_id},
    }
    return payload


def format_dataresource(
    df: pd.DataFrame,
    update: bool = False,
    display_id: Optional[str] = None,
    has_default_index: bool = True,
) -> tuple:
    display_id = display_id or str(uuid.uuid4())

    # determine original dataset size, and truncated/sampled size if it's beyond the limits
    orig_df_dimensions = get_df_dimensions(df, prefix="orig")
    df = sample_if_too_big(df, display_id=display_id)
    sampled_df_dimensions = get_df_dimensions(df, prefix="truncated")

    payload = generate_dataresource_body(df, display_id=display_id)

    dataframe_info = {
        "default_index_used": has_default_index,
        **orig_df_dimensions,
        **sampled_df_dimensions,
    }
    metadata = generate_metadata(display_id=display_id, **dataframe_info)

    if display_id not in DISPLAY_ID_TO_METADATA:
        DISPLAY_ID_TO_METADATA[display_id] = metadata

    payload = {dataresource_settings.DATARESOURCE_MEDIA_TYPE: payload}
    metadata = {dataresource_settings.DATARESOURCE_MEDIA_TYPE: metadata}

    # this needs to happen so we can update by display_id as needed
    with pd.option_context(
        "html.table_schema", dataresource_settings.DATARESOURCE_HTML_TABLE_SCHEMA
    ):
        logger.debug(f"displaying dataresource payload in {display_id=}")
        display(
            payload,
            raw=True,
            metadata=metadata,
            display_id=display_id,
            update=update,
        )

    return (payload, metadata)


def deregister(ipython_shell: Optional[InteractiveShell] = None) -> None:
    """
    Sets the current IPython display formatter as the dataresource
    display formatter, used for simpleTable / "classic DEX" outputs
    and updates global dx & pandas settings with dataresource settings.
    """
    if get_ipython() is None and ipython_shell is None:
        return

    global settings
    settings.DISPLAY_MODE = "simple"

    settings_to_apply = {
        "DISPLAY_MAX_COLUMNS",
        "DISPLAY_MAX_ROWS",
        "MEDIA_TYPE",
        "FLATTEN_INDEX_VALUES",
        "FLATTEN_COLUMN_VALUES",
        "STRINGIFY_INDEX_VALUES",
        "STRINGIFY_COLUMN_VALUES",
    }
    for setting in settings_to_apply:
        val = getattr(dataresource_settings, f"DATARESOURCE_{setting}", None)
        setattr(settings, setting, val)

    ipython = ipython_shell or get_ipython()

    custom_formatter = DXDataResourceDisplayFormatter()
    custom_formatter.formatters = DEFAULT_IPYTHON_DISPLAY_FORMATTER.formatters
    ipython.display_formatter = custom_formatter
