from typing import Optional

import pandas as pd
import structlog
from IPython.display import update_display

from dx.formatters.callouts import display_callout
from dx.settings import get_settings, settings_context
from dx.utils.tracking import (
    DATAFRAME_HASH_TO_VAR_NAME,
    DISPLAY_ID_TO_DATAFRAME_HASH,
    SUBSET_TO_DATAFRAME_HASH,
    generate_df_hash,
)

logger = structlog.get_logger(__name__)

settings = get_settings()


SUBSET_FILTERS = {}


def get_applied_filters(df: pd.DataFrame) -> dict:
    """
    Returns a dictionary of applied filters for a dataframe.
    """
    df_hash = generate_df_hash(df)
    return SUBSET_FILTERS.get(df_hash)


def update_display_id(
    display_id: str,
    sql_filter: str,
    pandas_filter: Optional[str] = None,
    filters: Optional[dict] = None,
    output_variable_name: Optional[str] = None,
    limit: Optional[int] = None,
) -> None:
    """
    Filters the dataframe in the cell with the given display_id.
    """
    from dx.utils.tracking import sql_engine

    global SUBSET_FILTERS

    row_limit = limit or settings.DISPLAY_MAX_ROWS
    df_hash = DISPLAY_ID_TO_DATAFRAME_HASH[display_id]
    df_name = DATAFRAME_HASH_TO_VAR_NAME[df_hash]
    table_name = f"{df_name}__{df_hash}"

    query_string = sql_filter.format(table_name=table_name)
    logger.debug(f"sql query string: {query_string}")
    new_df = pd.read_sql(query_string, sql_engine)

    # this is associating the subset with the original dataframe,
    # which will be checked when the DisplayFormatter.format() is called
    # during update_display(), which will prevent re-registering the display ID to the subset
    new_df_hash = generate_df_hash(new_df)

    # store filters to be passed through metadata to the frontend
    logger.debug(f"applying {filters=}")
    filters = filters or []
    SUBSET_FILTERS[new_df_hash] = filters

    logger.debug(f"assigning subset {new_df_hash} to parent {df_hash=}")
    SUBSET_TO_DATAFRAME_HASH[new_df_hash] = df_hash

    # allow temporary override of the display limit
    with settings_context(DISPLAY_MAX_ROWS=row_limit):
        logger.debug(f"updating {display_id=} with {min(row_limit, len(new_df))}-row resample")
        update_display(new_df, display_id=display_id)

    # we can't reference a variable type to suggest to users to perform a `df.query()`
    # type operation since it was never declared in the first place
    if not df_name.startswith("unk_dataframe_"):
        # TODO: replace with custom callout media type
        output_variable_name = output_variable_name or "new_df"
        filter_code = f"""{output_variable_name} = {df_name}.query("{pandas_filter.format(df_name=df_name)}", engine="python")"""
        filter_msg = f"""Copy the following snippet into a cell below to save this subset to a new dataframe:
        <pre style="background-color:white; padding:0.5rem; border-radius:5px;">{filter_code}</pre>
        """
        display_callout(
            filter_msg,
            header=False,
            icon="info",
            level="success",
            display_id=display_id + "-primary",
            update=True,
        )
