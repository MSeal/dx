from typing import Optional

import pandas as pd
import structlog
from IPython.display import update_display
from IPython.terminal.interactiveshell import InteractiveShell

from dx.sampling import get_df_dimensions
from dx.settings import get_settings, settings_context
from dx.types.filters import DEXFilterSettings, DEXResampleMessage
from dx.utils.tracking import (
    DXDF_CACHE,
    SUBSET_HASH_TO_PARENT_DATA,
    generate_df_hash,
    get_db_connection,
)

logger = structlog.get_logger(__name__)
db_connection = get_db_connection()
settings = get_settings()


def store_sample_to_history(df: pd.DataFrame, display_id: str, filters: list) -> dict:
    """
    Updates the metadata cache to include past filters, times, and dataframe info.
    """
    # apply new metadata for resampled dataset
    dxdf = DXDF_CACHE[display_id]

    metadata = dxdf.metadata
    datalink_metadata = metadata["datalink"]

    sample_time = pd.Timestamp("now").strftime(settings.DATETIME_STRING_FORMAT)
    # convert from FilterTypes to dicts
    dex_filters = [dex_filter.dict() for dex_filter in filters]
    sample = {
        "sampling_time": sample_time,
        "filters": dex_filters,
        "dataframe_info": get_df_dimensions(df, prefix="truncated"),
    }
    datalink_metadata["sample_history"].append(sample)
    # only storing the last n-number of samples, not everything
    datalink_metadata["sample_history"] = datalink_metadata["sample_history"][
        -settings.NUM_PAST_SAMPLES_TRACKED :
    ]
    datalink_metadata["applied_filters"] = dex_filters
    datalink_metadata["sampling_time"] = sample_time

    metadata["datalink"] = datalink_metadata
    dxdf.metadata = metadata

    return metadata


def resample_from_db(
    display_id: str,
    sql_filter: str,
    filters: Optional[list] = None,
    cell_id: Optional[str] = None,
    assign_subset: bool = True,
    ipython_shell: Optional[InteractiveShell] = None,
) -> pd.DataFrame:
    """
    Filters the dataframe in the cell with the given display_id.
    This is done by executing the SQL filter on the table
    associated with the given display ID.

    This also associates the queried subset to the original dataset
    (based on the display ID) so as to avoid re-registering a new
    display handler.
    """
    dxdf = DXDF_CACHE[display_id]
    # store filters to be passed through metadata to the frontend
    logger.debug(f"applying {filters=}")
    dxdf.filters = filters or []

    query_string = sql_filter.format(table_name=dxdf.variable_name)
    logger.debug(f"sql query string: {query_string}")
    new_df: pd.DataFrame = db_connection.execute(query_string).df()

    # just for logging purposes - not used anywhere
    count_resp = db_connection.execute(f"SELECT COUNT(*) FROM {dxdf.variable_name}").fetchone()
    # should return a tuple of (count,)
    orig_df_count = count_resp[0]
    logger.debug(f"filtered to {len(new_df)}/{orig_df_count} row(s)")

    # resetting original index if needed
    if dxdf.index_name is not None:
        new_df.set_index(dxdf.index_name, inplace=True)
    # convert back to original dtypes
    for col, dtype in dxdf.original_column_dtypes.items():
        if settings.FLATTEN_COLUMN_VALUES and isinstance(col, tuple):
            # the dataframe in use originally had pd.MultiIndex columns
            col = ", ".join(col)
        new_df[col] = new_df[col].astype(dtype)

    if assign_subset:
        # this is associating the subset with the original dataframe,
        # which will be checked when the DisplayFormatter.format() is called
        # during update_display(), which will prevent re-registering the display ID to the subset
        new_df_hash = generate_df_hash(new_df)
        logger.debug(f"assigning subset {cell_id}+{new_df_hash} to {display_id=}")
        SUBSET_HASH_TO_PARENT_DATA[new_df_hash] = {
            "cell_id": cell_id,
            "display_id": display_id,
        }

    return new_df


def handle_resample(
    msg: DEXResampleMessage,
    ipython_shell: Optional[InteractiveShell] = None,
) -> pd.DataFrame:
    raw_filters = msg.filters
    sample_size = msg.limit

    update_params = {
        "display_id": msg.display_id,
        "sql_filter": f"SELECT * FROM {{table_name}} LIMIT {sample_size}",
        "filters": raw_filters,
        "cell_id": msg.cell_id,
    }

    if raw_filters:
        dex_filters = DEXFilterSettings(filters=raw_filters)
        # used to actually filter the data
        sql_filter_str = dex_filters.to_sql_query()
        update_params[
            "sql_filter"
        ] = f"SELECT * FROM {{table_name}} WHERE {sql_filter_str} LIMIT {sample_size}"

        # TODO: move this into metadata?
        # used to give a pandas query string to the user
        # pandas_filter_str = dex_filters.to_pandas_query()

    resampled_df = resample_from_db(**update_params)

    metadata = store_sample_to_history(
        resampled_df,
        display_id=msg.display_id,
        filters=raw_filters,
    )

    # allow temporary override of the display
    context_params = dict(
        DISPLAY_MAX_ROWS=sample_size,
        DISPLAY_MAX_COLUMNS=msg.num_columns,
        COLUMN_SAMPLING_METHOD=msg.column_sampling_method,
        ROW_SAMPLING_METHOD=msg.row_sampling_method,
    )
    with settings_context(**context_params):
        logger.debug(
            f"updating {msg.display_id=} with {min(sample_size, len(resampled_df))}-row resample",
            **context_params,
        )
        update_display(
            resampled_df,
            display_id=msg.display_id,
            metadata=metadata,
        )

    return resampled_df
