import uuid
from functools import lru_cache
from typing import Optional, Set

import numpy as np
import pandas as pd
import structlog
from IPython import get_ipython
from IPython.core.formatters import DisplayFormatter
from IPython.core.interactiveshell import InteractiveShell
from IPython.display import HTML
from IPython.display import display as ipydisplay
from pandas.io.json import build_table_schema
from pydantic import BaseSettings, Field

from dx.config import DEFAULT_IPYTHON_DISPLAY_FORMATTER, IN_IPYTHON_ENV
from dx.filtering import register_display_id
from dx.sampling import sample_and_describe
from dx.settings import settings
from dx.utils import (
    df_is_subset,
    get_applied_filters,
    get_display_id,
    normalize_index_and_columns,
    to_dataframe,
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
    DATARESOURCE_STRINGIFY_INDEX_VALUES: bool = True
    DATARESOURCE_STRINGIFY_COLUMN_VALUES: bool = True

    class Config:
        validate_assignment = True  # we need this to enforce `allow_mutation`
        json_encoders = {type: lambda t: str(t)}


@lru_cache
def get_dataresource_settings():
    return DataResourceSettings()


dataresource_settings = get_dataresource_settings()

logger = structlog.get_logger(__name__)


class DXDataResourceDisplayFormatter(DisplayFormatter):
    def format(self, obj, **kwargs):

        if isinstance(obj, tuple(settings.RENDERABLE_OBJECTS)):
            if not isinstance(obj, pd.DataFrame):
                obj = to_dataframe(obj)
            update_existing_display = df_is_subset(obj)
            applied_filters = get_applied_filters(obj)
            display_id = get_display_id(obj)

            format_dataresource(
                obj,
                update=update_existing_display,
                display_id=display_id,
                filters=applied_filters,
            )

            # this needs to happen after sending to the frontend
            # so the user doesn't wait as long for writing to sqlite
            register_display_id(
                obj,
                display_id=display_id,
                is_subset=update_existing_display,
            )

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
    payload_body = {
        "schema": build_table_schema(df),
        "data": df.reset_index().to_dict("records"),
        "datalink": {},
    }
    payload = {dataresource_settings.DATARESOURCE_MEDIA_TYPE: payload_body}

    metadata_body = {
        "datalink": {
            "dataframe_info": {},
            "dx_settings": settings.json(exclude={"RENDERABLE_OBJECTS": True}),
            "applied_filters": [],
        },
    }
    metadata = {dataresource_settings.DATARESOURCE_MEDIA_TYPE: metadata_body}

    display_id = display_id or str(uuid.uuid4())
    payload_body["datalink"]["display_id"] = display_id
    metadata_body["datalink"]["display_id"] = display_id

    return (payload, metadata)


def format_dataresource(
    df: pd.DataFrame,
    update: bool = False,
    display_id: Optional[str] = None,
    filters: Optional[list] = None,
) -> tuple:
    # enable 0-n row counts for frontend
    df = normalize_index_and_columns(df)
    df, dataframe_info = sample_and_describe(df, display_id=display_id)
    payload, metadata = generate_dataresource_body(df, display_id=display_id)
    metadata[dataresource_settings.DATARESOURCE_MEDIA_TYPE]["datalink"].update(
        {
            "dataframe_info": dataframe_info,
            "applied_filters": filters,
        }
    )

    # don't pass a dataframe in here, otherwise you'll get recursion errors
    with pd.option_context(
        "html.table_schema", dataresource_settings.DATARESOURCE_HTML_TABLE_SCHEMA
    ):
        logger.debug(f"displaying dataresource payload in {display_id=}")
        ipydisplay(
            payload,
            raw=True,
            metadata=metadata,
            display_id=display_id,
            update=update,
        )

    # temporary placeholder for copy/paste user messaging
    ipydisplay(
        HTML("<div></div>"),
        display_id=display_id + "-primary",
        update=update,
    )

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

    settings_to_apply = {
        "DISPLAY_MAX_COLUMNS",
        "DISPLAY_MAX_ROWS",
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
    ipython.display_formatter = DXDataResourceDisplayFormatter()
