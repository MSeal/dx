import os
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
from dx.types.main import DXDisplayMode
from dx.utils.formatting import (
    check_for_duplicate_columns,
    generate_metadata,
    is_default_index,
    normalize_index_and_columns,
    to_dataframe,
)
from dx.utils.tracking import DXDF_CACHE, SUBSET_HASH_TO_PARENT_DATA, DXDataFrame, get_db_connection

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
    extra_metadata: Optional[dict] = None,
):
    dxdf = DXDataFrame(df)
    parent_display_id = determine_parent_display_id(dxdf)
    payload, metadata = format_output(
        dxdf.df,
        update=parent_display_id,
        display_id=dxdf.display_id,
        default_index_used=default_index_used,
        with_ipython_display=with_ipython_display,
        variable_name=dxdf.variable_name,
        extra_metadata=extra_metadata,
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
    extra_metadata: Optional[dict] = None,
):
    ipython = ipython_shell or get_ipython()

    logger.debug(f"*** handling {settings.DISPLAY_MODE} format for {type(obj)=} ***")
    if not isinstance(obj, pd.DataFrame):
        obj = to_dataframe(obj)
    obj = check_for_duplicate_columns(obj)
    logger.debug(f"{obj.shape=}")

    default_index_used = is_default_index(obj.index)

    if not settings.ENABLE_DATALINK:
        obj = normalize_index_and_columns(obj)
        payload, metadata = format_output(
            obj,
            default_index_used=default_index_used,
            with_ipython_display=with_ipython_display,
            extra_metadata=extra_metadata,
        )
        return payload, metadata

    try:
        payload, metadata = datalink_processing(
            obj,
            default_index_used,
            ipython_shell=ipython,
            with_ipython_display=with_ipython_display,
            extra_metadata=extra_metadata,
        )
    except Exception as e:
        logger.debug(f"Error in datalink_processing: {e}")
        # fall back to default processing
        payload, metadata = format_output(
            obj,
            default_index_used=default_index_used,
            with_ipython_display=with_ipython_display,
            extra_metadata=extra_metadata,
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
    schema = build_table_schema(df)
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
    extra_metadata: Optional[dict] = None,
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
        df=df,
        display_id=display_id,
        variable_name=variable_name,
        extra_metadata=extra_metadata,
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

    if settings.DEV_MODE:
        dev_display(payload, metadata)

    return (payload, metadata)


def determine_parent_display_id(dxdf: DXDataFrame) -> Optional[str]:
    """
    Before rendering a DataFrame, we need to check and see if this is the result
    of a resample request, which will appear as the same display ID and cell ID
    used to format the previous/original dataframe that we see here, which is used
    to update an existing display handler.
    - If the hash is the same, but the cell ID is different, we're executing in a different
    cell and should use a new (DXDataFrame-generated) display ID.
    - If the hash is different and found in SUBSET_HASH_TO_PARENT_DATA, we have a resample request
    result that's rendering a smaller subset of the original dataframe, and will
    update the existing display handler based on display ID.
    - If the hash is different and is *not* found in SUBSET_HASH_TO_PARENT_DATA, we have
    a new dataframe altogether, which should trigger a new output.
    """
    parent_dataset_info = SUBSET_HASH_TO_PARENT_DATA.get(dxdf.hash, {})

    parent_display_id = parent_dataset_info.get("display_id")
    no_parent_id = parent_display_id is None
    logger.debug(f"{dxdf.display_id=} & {parent_display_id=}")
    if no_parent_id:
        DXDF_CACHE[dxdf.display_id] = dxdf
    else:
        logger.debug(f"df is subset of existing {parent_display_id=}")

    last_executed_cell_id = os.environ.get("LAST_EXECUTED_CELL_ID")
    parent_cell_id = parent_dataset_info.get("cell_id")
    different_cell_output = parent_cell_id != dxdf.cell_id
    logger.debug(f"{dxdf.cell_id=} | {parent_cell_id=} | {last_executed_cell_id=}")
    if different_cell_output and parent_display_id is not None:
        logger.debug(
            f"disregarding {parent_display_id=} and using {dxdf.display_id=} since this is a new cell_id",
            parent_cell_id=parent_cell_id,
            cell_id=dxdf.cell_id,
        )
        # doesn't matter if this dataset was associated with another,
        # we shouldn't be re-rendering the display ID from another cell ID
        parent_display_id = None

    if parent_display_id is not None:
        logger.debug(
            f"updating existing display handler {parent_display_id=}",
            parent_cell_id=parent_cell_id,
            cell_id=dxdf.cell_id,
        )
        # if we don't remove this, we'll keep updating the same display handler
        SUBSET_HASH_TO_PARENT_DATA.pop(dxdf.hash)
    return parent_display_id


def dev_display(payload, metadata):

    from IPython.display import JSON, display

    display(JSON({"payload": payload}))
    display(JSON({"metadata": metadata}))
