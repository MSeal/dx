import html
from typing import Optional

import pandas as pd
import structlog
from IPython.display import update_display

from dx.formatters.callouts import display_callout
from dx.sampling import get_df_dimensions
from dx.settings import get_settings, settings_context
from dx.utils.tracking import (
    DATAFRAME_HASH_TO_VAR_NAME,
    DISPLAY_ID_TO_DATAFRAME_HASH,
    DISPLAY_ID_TO_DATETIME_COLUMNS,
    DISPLAY_ID_TO_INDEX,
    DISPLAY_ID_TO_SEQUENCE_COLUMNS,
    SUBSET_TO_DATAFRAME_HASH,
    generate_df_hash,
)

logger = structlog.get_logger(__name__)

settings = get_settings()


def store_sample_to_history(df: pd.DataFrame, display_id: str, filters: list) -> dict:
    """
    Updates the metadata cache to include past filters, times, and dataframe info.
    """
    global DISPLAY_ID_TO_METADATA

    # apply new metadata for resampled dataset
    metadata = DISPLAY_ID_TO_METADATA[display_id]
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
    DISPLAY_ID_TO_METADATA[display_id] = metadata

    # don't return metadata to pass into update_display(), since will
    # trigger another initial render and will recreate the metadata
    # inside


def update_display_id(
    display_id: str,
    sql_filter: str,
    pandas_filter: Optional[str] = None,
    filters: Optional[list] = None,
    output_variable_name: Optional[str] = None,
    limit: Optional[int] = None,
) -> None:
    """
    Filters the dataframe in the cell with the given display_id.
    """
    from dx.utils.tracking import sql_engine

    global DISPLAY_ID_TO_FILTERS

    row_limit = limit or settings.DISPLAY_MAX_ROWS
    df_hash = DISPLAY_ID_TO_DATAFRAME_HASH[display_id]
    df_name = DATAFRAME_HASH_TO_VAR_NAME[df_hash]
    table_name = f"{df_name}__{df_hash}"

    query_string = sql_filter.format(table_name=table_name)
    logger.debug(f"sql query string: {query_string}")
    new_df = pd.read_sql(query_string, sql_engine)
    logger.debug(f"{new_df.columns=}")

    with sql_engine.connect() as conn:
        orig_df_count = conn.execute(f"SELECT COUNT (*) FROM {table_name}").scalar()
    logger.debug(f"filtered to {len(new_df)}/{orig_df_count} row(s)")

    store_sample_to_history(new_df, display_id=display_id, filters=filters)

    # in the event there were nested values stored,
    # try to expand them back to their original datatypes
    for col in new_df.columns:
        if col in DISPLAY_ID_TO_SEQUENCE_COLUMNS[display_id]:
            new_df[col] = new_df[col].apply(lambda x: x.split(", "))
    # resetting original formatting
    if display_id in DISPLAY_ID_TO_INDEX:
        index_col = DISPLAY_ID_TO_INDEX[display_id] or "index"
        new_df.set_index(index_col, inplace=True)
    if display_id in DISPLAY_ID_TO_DATETIME_COLUMNS:
        for col in DISPLAY_ID_TO_DATETIME_COLUMNS[display_id]:
            new_df[col] = pd.to_datetime(new_df[col])

    # this is associating the subset with the original dataframe,
    # which will be checked when the DisplayFormatter.format() is called
    # during update_display(), which will prevent re-registering the display ID to the subset
    new_df_hash = generate_df_hash(new_df)

    # store filters to be passed through metadata to the frontend
    logger.debug(f"applying {filters=}")
    filters = filters or []
    DISPLAY_ID_TO_FILTERS[display_id] = filters

    logger.debug(f"assigning subset {new_df_hash} to parent {df_hash=}")
    SUBSET_TO_DATAFRAME_HASH[new_df_hash] = df_hash

    # allow temporary override of the display limit
    with settings_context(DISPLAY_MAX_ROWS=row_limit):
        logger.debug(f"updating {display_id=} with {min(row_limit, len(new_df))}-row resample")
        update_display(
            new_df,
            display_id=display_id,
        )

    # we can't reference a variable type to suggest to users to perform a `df.query()`
    # type operation since it was never declared in the first place
    if not df_name.startswith("unk_dataframe_"):
        # TODO: replace with custom callout media type
        output_variable_name = output_variable_name or "new_df"
        # wrapping the triple quotes internally so the user can copy/paste directly
        # without worry of double/single quotes in their data not being handled
        pandas_query_str = f'"""{pandas_filter.format(df_name=df_name)}"""'
        filter_code = (
            f"""{output_variable_name} = {df_name}.query({pandas_query_str}, engine="python")"""
        )
        filter_msg = f"""Copy the following snippet into a cell below to save this subset to a new dataframe:
        <pre style="background-color:white; padding:0.5rem; border-radius:5px;">{html.escape(filter_code, quote=True)}</pre>
        """
        display_callout(
            filter_msg,
            header=False,
            icon="info",
            level="success",
            display_id=display_id + "-primary",
            update=True,
        )
