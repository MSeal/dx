import hashlib
import os
import uuid
from typing import Optional

import pandas as pd
from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell
from IPython.display import update_display
from pandas.util import hash_pandas_object
from sqlalchemy import create_engine

from dx.formatters.callouts import display_callout
from dx.loggers import get_logger
from dx.settings import get_settings, set_option

DATAFRAME_HASH_TO_DISPLAY_ID = {}
DATAFRAME_HASH_TO_VAR_NAME = {}
DISPLAY_ID_TO_COLUMNS = {}
DISPLAY_ID_TO_DATAFRAME_HASH = {}
SUBSET_TO_DATAFRAME_HASH = {}
SUBSET_FILTERS = {}

logger = get_logger(__name__)

settings = get_settings()

sql_engine = create_engine("sqlite://", echo=False)


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
    orig_sample_size = int(settings.DISPLAY_MAX_ROWS)
    set_option("DISPLAY_MAX_ROWS", row_limit)
    logger.debug(f"updating {display_id=} with {min(row_limit, len(new_df))}-row resample")
    update_display(new_df, display_id=display_id)
    set_option("DISPLAY_MAX_ROWS", orig_sample_size)

    # TODO: replace with custom callout media type
    callout_display_id = display_id + "-primary"
    output_variable_name = output_variable_name or "new_df"
    filter_code = f"""{output_variable_name} = {df_name}.query({pandas_filter}, engine="python")"""
    filter_msg = f"""Copy the following snippet into a cell below to save this subset to a new dataframe:
    <pre style="background-color:white; padding:0.5rem; border-radius:5px;">{filter_code}</pre>
    """
    display_callout(
        filter_msg,
        header=False,
        icon="info",
        level="success",
        display_id=callout_display_id,
    )


def get_display_id_for_df(df: pd.DataFrame) -> str:
    df_hash = generate_df_hash(df)
    return DATAFRAME_HASH_TO_DISPLAY_ID.get(df_hash)


def generate_df_hash(df: pd.DataFrame) -> str:
    """
    Original df:
              0         1         2         3         4
    0  0.230950  0.766084  0.913629  0.133418  0.916593
    1  0.156634  0.103393  0.373932  0.619625  0.386718
    2  0.204738  0.411156  0.172771  0.502443  0.484988
    3  0.026402  0.248560  0.260528  0.064049  0.831178
    4  0.911507  0.261114  0.618599  0.984881  0.128810

    After hash_pandas_object():
    0    14963028434725389246
    1    13734102023063095786
    2    14568529259697808682
    3     1257782805939107919
    4    10935027788698945420
    dtype: uint64

    String-concatenating the hash series values:
    '14963028434725389246-13734102023063095786-14568529259697808682-1257782805939107919-10935027788698945420'

    SHA256 hash:
    'd3148913511e79be9b301d5ef665196a889b53cce82643b9fdee9d25403828b8'
    """
    # this will be a series of hash values the length of df
    df_hash_series = hash_pandas_object(df)
    # then string-concatenate all the hashed values, which could be very large
    df_hash_str = "-".join(df_hash_series.astype(str))
    # then hash the resulting (potentially large) string
    hash_str = hashlib.sha256(df_hash_str.encode()).hexdigest()
    return hash_str


def get_cell_id() -> str:
    return os.environ.get("LAST_EXECUTED_CELL_ID")


def get_df_variable_name(
    df: pd.DataFrame,
    ipython_shell: Optional[InteractiveShell] = None,
) -> str:
    """
    Returns the variable name of the DataFrame object.
    """
    ipython = ipython_shell or get_ipython()
    df_vars = {k: v for k, v in ipython.user_ns.items() if isinstance(v, pd.DataFrame)}
    logger.debug(f"dataframe variables present: {list(df_vars.keys())}")

    matching_df_vars = [
        k for k, v in df_vars.items() if generate_df_hash(v) == generate_df_hash(df)
    ]
    # we might get a mix of references here like ['_', '__', 'df']
    named_df_vars_with_same_hash = [name for name in matching_df_vars if not name.startswith("_")]
    if named_df_vars_with_same_hash:
        logger.debug(f"{named_df_vars_with_same_hash=}")
        return named_df_vars_with_same_hash[0]

    if df_vars:
        # dataframe rendered without variable assignment
        logger.debug(f"no matching dataframe variables found: {matching_df_vars=}")
        return matching_df_vars[-1]

    # no dataframe variables found, assign a new one for internal referencing
    logger.debug("no dataframe variables found")
    return f"unk_dataframe_{uuid.uuid4()}"


def register_display_id(
    df: pd.DataFrame,
    display_id: str,
    ipython_shell: Optional[InteractiveShell] = None,
) -> None:
    from dx.utils import handle_column_dtypes

    global DATAFRAME_HASH_TO_DISPLAY_ID
    global DATAFRAME_HASH_TO_VAR_NAME
    global DISPLAY_ID_TO_DATAFRAME_HASH
    global DISPLAY_ID_TO_COLUMNS

    df_hash = generate_df_hash(df)
    DISPLAY_ID_TO_DATAFRAME_HASH[display_id] = df_hash
    DATAFRAME_HASH_TO_DISPLAY_ID[df_hash] = display_id

    df_name = get_df_variable_name(df, ipython_shell=ipython_shell)
    DATAFRAME_HASH_TO_VAR_NAME[df_hash] = df_name
    logger.debug(f"registering display_id {display_id=} for `{df_name}`")

    # make sure any dtypes/geometries/etc are converted
    for column in df.columns:
        df[column] = handle_column_dtypes(df[column])

    # prepending the hash to avoid any "unrecognized token" SQL errors
    table_name = f"{df_name}__{df_hash}"
    logger.debug(f"writing to `{table_name}` table in sqlite")
    with sql_engine.begin() as conn:
        num_written_rows = df.to_sql(table_name, con=conn, if_exists="replace")
    logger.debug(f"wrote {num_written_rows} row(s) to `{table_name}` table")
