from typing import Optional

import pandas as pd
import structlog
from IPython.display import update_display

from dx.sampling import get_df_dimensions
from dx.settings import get_settings, settings_context
from dx.types import DEXFilterSettings
from dx.utils.tracking import (
    DISPLAY_ID_TO_FILTERS,
    DXDataFrameCache,
    cache_manager,
    generate_df_hash,
    sql_engine,
)

logger = structlog.get_logger(__name__)

settings = get_settings()


def store_sample_to_history(df: pd.DataFrame, display_id: str, filters: list) -> dict:
    """
    Updates the metadata cache to include past filters, times, and dataframe info.
    """
    # apply new metadata for resampled dataset
    dfc: DXDataFrameCache = cache_manager.get_by_display_id(display_id)
    metadata = dfc.metadata
    datalink_metadata = metadata["datalink"]

    sample_time = pd.Timestamp("now").strftime(settings.DATETIME_STRING_FORMAT)
    sample = {
        "sampling_time": sample_time,
        "filters": filters,
        "dataframe_info": get_df_dimensions(df, prefix="truncated"),
    }
    datalink_metadata["sample_history"].append(sample)
    # only storing the last n-number of samples, not everything
    datalink_metadata["sample_history"] = datalink_metadata["sample_history"][
        -settings.NUM_PAST_SAMPLES_TRACKED :
    ]
    datalink_metadata["applied_filters"] = filters
    datalink_metadata["sampling_time"] = sample_time

    metadata["datalink"] = datalink_metadata
    dfc.metadata = metadata

    return metadata


def update_display_id(
    display_id: str,
    sql_filter: str,
    pandas_filter: Optional[str] = None,
    filters: Optional[list] = None,
    output_variable_name: Optional[str] = None,
    limit: Optional[int] = None,
    cell_id: Optional[str] = None,
) -> None:
    """
    Filters the dataframe in the cell with the given display_id.
    This is done by executing the SQL filter on the table
    associated with the given display ID.

    This also associates the queried subset to the original dataset
    (based on the display ID) so as to avoid re-registering a new
    display handler.
    """
    row_limit = limit or settings.DISPLAY_MAX_ROWS
    dfc: DXDataFrameCache = cache_manager.get_by_display_id(display_id)

    query_string = sql_filter.format(table_name=dfc.sql_table)
    logger.debug(f"sql query string: {query_string}")
    new_df = pd.read_sql(query_string, sql_engine)

    with sql_engine.connect() as conn:
        orig_df_count = conn.execute(f"SELECT COUNT (*) FROM {dfc.sql_table}").scalar()
    logger.debug(f"filtered to {len(new_df)}/{orig_df_count} row(s)")

    metadata = store_sample_to_history(new_df, display_id=display_id, filters=filters)

    # in the event there were nested values stored,
    # try to expand them back to their original datatypes
    for col in new_df.columns:
        if col in dfc.sequence_columns:
            new_df[col] = new_df[col].apply(lambda x: x.split(", "))

    # resetting original index
    new_df.set_index(dfc.index_name, inplace=True)

    # convert back to original dtypes
    for col, dtype in dfc.original_column_dtypes.items():
        new_df[col] = new_df[col].astype(dtype)

    # this is associating the subset with the original dataframe,
    # which will be checked when the DisplayFormatter.format() is called
    # during update_display(), which will prevent re-registering the display ID to the subset
    new_df_hash = generate_df_hash(new_df)

    # store filters to be passed through metadata to the frontend
    logger.debug(f"applying {filters=}")
    filters = filters or []
    DISPLAY_ID_TO_FILTERS[display_id] = filters

    logger.debug(f"assigning subset {new_df_hash} to parent {dfc.hash=}")
    cache_manager.filter_subsets[new_df_hash] = dfc.hash

    # allow temporary override of the display limit
    with settings_context(DISPLAY_MAX_ROWS=row_limit):
        logger.debug(f"updating {display_id=} with {min(row_limit, len(new_df))}-row resample")
        update_display(
            new_df,
            display_id=display_id,
            metadata=metadata,
        )


def handle_resample(data: dict) -> None:
    # TODO: add resample message to types.py
    # `data` should look like this:
    # {
    #     "display_id": "1c1c8b40-f1f4-4205-931d-644a42e8232d",
    #     "sampling": {
    #         "filters": [
    #             {
    #                 "column": "float_column",
    #                 "type": "METRIC_FILTER",
    #                 "predicate": "between",
    #                 "value": [0.5346270287577823, 0.673002123739554],
    #             }
    #         ],
    #         "sample_size": 10000,
    #     },
    #     "status": "submitted",
    #     "cell_id": "cell1",   # <-- not currently used
    # }

    raw_filters = data["filters"]
    sample_size = data["limit"]

    update_params = {
        "display_id": data["display_id"],
        "sql_filter": f"SELECT * FROM {{table_name}} LIMIT {sample_size}",
        "filters": raw_filters,
        "limit": sample_size,
        "cell_id": data["cell_id"],
    }

    if raw_filters:
        dex_filters = DEXFilterSettings(filters=raw_filters)
        # used to give a pandas query string to the user
        pandas_filter_str = dex_filters.to_pandas_query()
        # used to actually filter the data
        sql_filter_str = dex_filters.to_sql_query()
        update_params.update(
            {
                "pandas_filter": pandas_filter_str,
                "sql_filter": f"SELECT * FROM {{table_name}} WHERE {sql_filter_str} LIMIT {sample_size}",
                "filters": raw_filters,
            }
        )

    update_display_id(**update_params)
