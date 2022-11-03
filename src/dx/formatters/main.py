import uuid
from typing import Optional

import pandas as pd
import structlog
from IPython import get_ipython
from IPython.core.formatters import DisplayFormatter
from IPython.core.interactiveshell import InteractiveShell
from IPython.display import display as ipydisplay
from pandas.io.json import build_table_schema

from dx.sampling import get_df_dimensions, sample_if_too_big
from dx.settings import settings
from dx.types import DXDisplayMode
from dx.utils.formatting import (
    generate_metadata,
    is_default_index,
    normalize_index_and_columns,
    to_dataframe,
)
from dx.utils.tracking import DXDF_CACHE, SUBSET_TO_DISPLAY_ID, DXDataFrame, get_db_connection

logger = structlog.get_logger(__name__)
db_connection = get_db_connection()

DEFAULT_IPYTHON_DISPLAY_FORMATTER = DisplayFormatter()
IN_NOTEBOOK_ENV = False
if get_ipython() is not None:
    DEFAULT_IPYTHON_DISPLAY_FORMATTER = get_ipython().display_formatter

    try:
        from ipykernel.zmqshell import ZMQInteractiveShell

        IN_NOTEBOOK_ENV = isinstance(get_ipython(), ZMQInteractiveShell)
    except ImportError:
        pass


def datalink_processing(
    df: pd.DataFrame,
    default_index_used: bool,
    ipython_shell: Optional[InteractiveShell] = None,
    with_ipython_display: bool = True,
):
    dxdf = DXDataFrame(df)
    logger.debug(f"{dxdf=}")

    parent_display_id = SUBSET_TO_DISPLAY_ID.get(dxdf.hash)
    if parent_display_id is None:
        DXDF_CACHE[dxdf.display_id] = dxdf
        logger.debug(f"{DXDF_CACHE=}")
    else:
        logger.debug(f"df is subset of existing {parent_display_id=}")

    payload, metadata = format_output(
        dxdf.df,
        update=parent_display_id,
        display_id=dxdf.display_id,
        default_index_used=default_index_used,
        with_ipython_display=with_ipython_display,
        variable_name=dxdf.variable_name,
    )

    # this needs to happen after sending to the frontend
    # so the user doesn't wait as long for writing larger datasets
    if not parent_display_id:
        logger.debug(f"registering `{dxdf.variable_name}` to duckdb")
        db_connection.register(dxdf.variable_name, dxdf.df.reset_index())

    return payload, metadata


def handle_format(
    obj,
    with_ipython_display: bool = True,
    ipython_shell: Optional[InteractiveShell] = None,
):
    ipython = ipython_shell or get_ipython()

    logger.debug(f"*** handling {settings.DISPLAY_MODE} format for {type(obj)=} ***")
    if not isinstance(obj, pd.DataFrame):
        obj = to_dataframe(obj)
    logger.debug(f"{obj.shape=}")

    default_index_used = is_default_index(obj.index)

    if not settings.ENABLE_DATALINK:
        obj = normalize_index_and_columns(obj)
        payload, metadata = format_output(
            obj,
            default_index_used=default_index_used,
            with_ipython_display=with_ipython_display,
        )
        return payload, metadata

    try:
        payload, metadata = datalink_processing(
            obj,
            default_index_used,
            ipython_shell=ipython,
            with_ipython_display=with_ipython_display,
        )
    except Exception as e:
        logger.debug(f"Error in datalink_processing: {e}")
        # fall back to default processing
        payload, metadata = format_output(
            obj,
            default_index_used=default_index_used,
            with_ipython_display=with_ipython_display,
        )

    return payload, metadata


class DXDisplayFormatter(DisplayFormatter):
    formatters = DEFAULT_IPYTHON_DISPLAY_FORMATTER.formatters

    def format(self, obj, **kwargs):

        if IN_NOTEBOOK_ENV and isinstance(obj, tuple(settings.RENDERABLE_OBJECTS)):
            handle_format(obj)
            return ({}, {})

        return DEFAULT_IPYTHON_DISPLAY_FORMATTER.format(obj, **kwargs)


def generate_body(
    df: pd.DataFrame,
    display_id: Optional[str] = None,
    default_index_used: bool = True,
) -> tuple:
    """
    Transforms the dataframe to a payload dictionary containing the
    table schema and transformed tabular data based on the current
    display mode.
    """
    schema = build_table_schema(df, index=default_index_used)
    logger.debug(f"{schema=}")

    # This is a little odd, but it allows replacing `pd.NA` and np.nan
    # with `None` values without altering any of the other values.
    # Without converting to `object`, `NaN`s will persist (but `pd.NA`s
    # will be converted to `None`).
    # We build the schema first since, after this, the dtypes will be
    # changed to `object` for any Series whose values were replaced with `None`s.
    clean_df = df.astype(object).where(df.notnull(), None)

    if settings.DISPLAY_MODE == DXDisplayMode.simple:
        data = clean_df.reset_index().to_dict("records")
    elif settings.DISPLAY_MODE == DXDisplayMode.enhanced:
        data = clean_df.reset_index().transpose().values.tolist()

    payload = {
        "schema": schema,
        "data": data,
        "datalink": {"display_id": display_id},
    }
    return payload


def format_output(
    df: pd.DataFrame,
    update: bool = False,
    display_id: Optional[str] = None,
    default_index_used: bool = True,
    with_ipython_display: bool = True,
    variable_name: str = "",
) -> tuple:
    display_id = display_id or str(uuid.uuid4())

    # determine original dataset size, and truncated/sampled size if it's beyond the limits
    orig_df_dimensions = get_df_dimensions(df, prefix="orig")
    df = sample_if_too_big(df, display_id=display_id)
    sampled_df_dimensions = get_df_dimensions(df, prefix="truncated")

    payload = generate_body(
        df,
        display_id=display_id,
        default_index_used=default_index_used,
    )

    dataframe_info = {
        "default_index_used": default_index_used,
        **orig_df_dimensions,
        **sampled_df_dimensions,
    }
    metadata = generate_metadata(
        display_id=display_id,
        variable_name=variable_name,
        **dataframe_info,
    )

    payload = {settings.MEDIA_TYPE: payload}
    metadata = {settings.MEDIA_TYPE: metadata}

    # this needs to happen so we can update by display_id as needed
    if with_ipython_display:
        with pd.option_context("html.table_schema", settings.HTML_TABLE_SCHEMA):
            logger.debug(f"displaying {settings.MEDIA_TYPE} payload in {display_id=}")
            ipydisplay(
                payload,
                raw=True,
                metadata=metadata,
                display_id=display_id,
                update=update,
            )

    return (payload, metadata)
