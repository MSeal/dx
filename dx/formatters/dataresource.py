import uuid
from functools import lru_cache
from typing import Optional, Set

import numpy as np
import pandas as pd
import structlog
from IPython import get_ipython
from IPython.core.formatters import BaseFormatter
from IPython.core.interactiveshell import InteractiveShell
from pandas.io.json import build_table_schema
from pydantic import BaseSettings, Field

from dx.filtering import SUBSET_FILTERS
from dx.sampling import sample_and_describe
from dx.settings import settings
from dx.utils.datatypes import to_dataframe
from dx.utils.formatting import is_default_index, normalize_index_and_columns
from dx.utils.tracking import (
    SUBSET_TO_DATAFRAME_HASH,
    generate_df_hash,
    get_display_id,
    register_display_id,
    store_in_sqlite,
)


class DataResourceSettings(BaseSettings):
    # "simple" (classic simpleTable/DEX) display mode
    DATARESOURCE_DISPLAY_MAX_ROWS: int = 100_000
    DATARESOURCE_DISPLAY_MAX_COLUMNS: int = 50
    DATARESOURCE_HTML_TABLE_SCHEMA: bool = Field(True, allow_mutation=False)
    DATARESOURCE_MEDIA_TYPE: str = Field("application/vnd.dataresource+json", allow_mutation=False)
    DATARESOURCE_RENDERABLE_OBJECTS: Set[type] = {pd.Series, pd.DataFrame, np.ndarray}

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


def handle_dataresource_format(obj):
    logger.debug(f"*** handling dataresource format for {type(obj)=} ***")
    if not isinstance(obj, pd.DataFrame):
        obj = to_dataframe(obj)

    default_index_used = is_default_index(obj.index)
    obj = normalize_index_and_columns(obj)

    if not settings.ENABLE_DATALINK:
        payload, metadata = format_dataresource(
            obj,
            has_default_index=default_index_used,
        )
        return payload, metadata

    obj_hash = generate_df_hash(obj)
    update_existing_display = obj_hash in SUBSET_TO_DATAFRAME_HASH
    applied_filters = SUBSET_FILTERS.get(obj_hash)
    display_id = get_display_id(obj_hash)
    sqlite_df_table = register_display_id(
        obj,
        display_id=display_id,
        df_hash=obj_hash,
        is_subset=update_existing_display,
    )

    payload, metadata = format_dataresource(
        obj,
        update=update_existing_display,
        display_id=display_id,
        filters=applied_filters,
        has_default_index=default_index_used,
    )

    # this needs to happen after sending to the frontend
    # so the user doesn't wait as long for writing larger datasets
    store_in_sqlite(sqlite_df_table, obj)
    return payload, metadata


class DXDataResourceDisplayFormatter(BaseFormatter):
    print_method = "_repr_data_resource_"
    _return_type = (dict,)


def generate_dataresource_body(
    df: pd.DataFrame,
    display_id: Optional[str] = None,
) -> tuple:
    """
    Transforms the dataframe to a payload dictionary containing the
    table schema and column values as arrays.
    """
    payload = {
        "schema": build_table_schema(df),
        "data": df.reset_index().to_dict("records"),
        "datalink": {"display_id": display_id},
    }

    metadata = {
        "datalink": {
            "dataframe_info": {},
            "dx_settings": settings.json(exclude={"RENDERABLE_OBJECTS": True}),
            "applied_filters": [],
            "display_id": display_id,
        },
        "display_id": display_id,
    }
    return (payload, metadata)


def format_dataresource(
    df: pd.DataFrame,
    update: bool = False,
    display_id: Optional[str] = None,
    filters: Optional[list] = None,
    has_default_index: bool = True,
) -> tuple:
    display_id = display_id or str(uuid.uuid4())
    df, dataframe_info = sample_and_describe(df, display_id=display_id)
    dataframe_info["default_index_used"] = has_default_index
    payload, metadata = generate_dataresource_body(df, display_id=display_id)
    metadata["datalink"].update(
        {
            "dataframe_info": dataframe_info,
            "applied_filters": filters,
        }
    )

    # TODO: figure out a way to mimic this behavior since it was helpful
    # having a display handle that we could update in place,
    # but that went through as a display_data message, instead of execute_result
    # and we can't do it with BaseFormatter, otherwise we'll double-render
    # with pd.option_context(
    #     "html.table_schema", dataresource_settings.DATARESOURCE_HTML_TABLE_SCHEMA
    # ):
    #     logger.debug(f"displaying dataresource payload in {display_id=}")
    #     ipydisplay(
    #         payload,
    #         raw=True,
    #         metadata=metadata,
    #         display_id=display_id,
    #         update=update,
    #     )

    # # temporary placeholder for copy/paste user messaging
    # ipydisplay(
    #     HTML("<div></div>"),
    #     display_id=display_id + "-primary",
    #     update=update,
    # )
    return (payload, metadata)


def deregister(ipython_shell: Optional[InteractiveShell] = None) -> None:
    """
    Sets the current IPython display formatter as the dataresource
    display formatter, used for simpleTable / "classic DEX" outputs
    and updates global dx & pandas settings with dataresource settings.
    """
    from dx.formatters.dx import get_dx_settings

    if get_ipython() is None and ipython_shell is None:
        return

    global settings
    settings.DISPLAY_MODE = "simple"

    settings_to_apply = {
        "DISPLAY_MAX_COLUMNS",
        "DISPLAY_MAX_ROWS",
        "HTML_TABLE_SCHEMA",
        "MEDIA_TYPE",
        "RENDERABLE_OBJECTS",
        "FLATTEN_INDEX_VALUES",
        "FLATTEN_COLUMN_VALUES",
        "STRINGIFY_INDEX_VALUES",
        "STRINGIFY_COLUMN_VALUES",
    }
    for setting in settings_to_apply:
        val = getattr(dataresource_settings, f"DATARESOURCE_{setting}", None)
        setattr(settings, setting, val)

    ipython = ipython_shell or get_ipython()

    # https://github.com/pandas-dev/pandas/blob/ad190575aa75962d2d0eade2de81a5fe5a2e285b/pandas/io/formats/printing.py#L244
    # https://github.com/pandas-dev/pandas/blob/926b9ceff10d9b7a957811f0a4de3167332196de/pandas/io/formats/printing.py?q=_repr_data_resource_#L268
    # https://ipython.readthedocs.io/en/stable/config/integrating.html#formatters-for-third-party-types
    # https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html#:~:text=plain.for_type(int%2C%20int_formatter)
    formatters = ipython.display_formatter.formatters
    mimetype = dataresource_settings.DATARESOURCE_MEDIA_TYPE

    formatters[mimetype] = DXDataResourceDisplayFormatter()
    for obj in settings.RENDERABLE_OBJECTS:
        formatters[mimetype].for_type(obj, handle_dataresource_format)
    formatters[mimetype].enabled = True

    for other_media_type in [get_dx_settings().DX_MEDIA_TYPE]:
        if other_media_type in formatters:
            del formatters[other_media_type]
