import hashlib
import uuid
from typing import Optional

import pandas as pd
import structlog
from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell
from pandas.util import hash_pandas_object
from sqlalchemy import create_engine

from dx.utils.datatypes import has_numeric_strings, is_sequence_series
from dx.utils.date_time import is_datetime_series
from dx.utils.formatting import (
    clean_column_values_for_hash,
    clean_column_values_for_sqlite,
    normalize_index_and_columns,
)

logger = structlog.get_logger(__name__)
sql_engine = create_engine("sqlite://", echo=False)


# we need to keep track of some things here:
# - an original uuid for each dataframe
# - the hash of each dataframe so we aren't storing them multiple times
# - the display ID associated with each *cleaned* dataframe
# - the cell ID associated with the display ID, when passed during an update over comms
# - before/after cleaning associations per dataframe
# - any special column treatment (e.g. datetime columns)
# TODO: create new classes to handle this instead of abusing globals.

CELL_ID_TO_DISPLAY_ID = {}

DATAFRAME_HASH_TO_DISPLAY_ID = {}
DATAFRAME_HASH_TO_VAR_NAME = {}

DISPLAY_ID_TO_COLUMNS = {}
DISPLAY_ID_TO_DATAFRAME_HASH = {}
DISPLAY_ID_TO_METADATA = {}
DISPLAY_ID_TO_FILTERS = {}

DISPLAY_ID_TO_INDEX = {}
DISPLAY_ID_TO_ORIG_COLUMN_DTYPES = {}
DISPLAY_ID_TO_DATETIME_COLUMNS = {}
DISPLAY_ID_TO_CONVERTED_COLUMNS = {}
DISPLAY_ID_TO_SEQUENCE_COLUMNS = {}

SUBSET_TO_DATAFRAME_HASH = {}


def get_display_id_for_df(df: pd.DataFrame) -> str:
    df_hash = generate_df_hash(df)
    return DATAFRAME_HASH_TO_DISPLAY_ID.get(df_hash)


def generate_df_hash(df: pd.DataFrame) -> str:
    """
    Generates a single hash string for the dataframe object.

    Example
    ----------------
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

    String-concatenate the hash series values:
    '14963028434725389246-13734102023063095786-14568529259697808682-1257782805939107919-10935027788698945420'

    SHA256 hash the string-concatenated values:
    'd3148913511e79be9b301d5ef665196a889b53cce82643b9fdee9d25403828b8'
    """
    hash_df = df.copy()

    for col in hash_df.columns:
        hash_df[col] = clean_column_values_for_hash(hash_df[col])

    # this will be a series of hash values the length of df
    df_hash_series = hash_pandas_object(hash_df)
    # then string-concatenate all the hashed values, which could be very large
    df_hash_str = "-".join(df_hash_series.astype(str))
    # then hash the resulting (potentially large) string
    hash_str = hashlib.sha256(df_hash_str.encode()).hexdigest()
    return hash_str


def is_equal(df: pd.DataFrame, other_df: pd.DataFrame, df_hash: str):
    if df.shape != other_df.shape:
        return False
    if sorted(list(df.columns)) != sorted(list(other_df.columns)):
        return False

    # this could be expensive, so we only want to do it if we're
    # pretty sure two dataframes could be equal
    logger.debug("-- cleaning before hashing --")
    other_hash = generate_df_hash(normalize_index_and_columns(other_df))
    if df_hash != other_hash:
        return False

    return True


def get_df_variable_name(
    df: pd.DataFrame,
    ipython_shell: Optional[InteractiveShell] = None,
    df_hash: Optional[str] = None,
) -> str:
    """
    Returns the variable name of the DataFrame object.
    """
    ipython = ipython_shell or get_ipython()
    df_vars = {k: v for k, v in ipython.user_ns.items() if isinstance(v, pd.DataFrame)}
    logger.debug(f"dataframe variables present: {list(df_vars.keys())}")

    df_hash = df_hash or generate_df_hash(df)
    matching_df_vars = [k for k, v in df_vars.items() if is_equal(df, v, df_hash)]

    # we might get a mix of references here like ['_', '__', 'df']
    named_df_vars_with_same_hash = [name for name in matching_df_vars if not name.startswith("_")]
    if named_df_vars_with_same_hash:
        logger.debug(f"{named_df_vars_with_same_hash=}")
        return named_df_vars_with_same_hash[0]

    if matching_df_vars:
        # dataframe rendered without variable assignment
        logger.debug(f"no matching dataframe variables found: {matching_df_vars=}")
        return matching_df_vars[-1]

    # no dataframe variables found, assign a new one for internal referencing
    logger.debug("no variables found matching this dataframe")
    df_uuid = f"unk_dataframe_{uuid.uuid4()}".replace("-", "")
    return df_uuid


def register_display_id(
    df: pd.DataFrame,
    display_id: str,
    df_hash: str,
    ipython_shell: Optional[InteractiveShell] = None,
) -> str:
    """
    Hashes the dataframe object and tracks display_id for future references in other function calls,
    and writes the data to a local sqlite table for follow-on SQL querying.
    """
    DISPLAY_ID_TO_DATAFRAME_HASH[display_id] = df_hash
    DATAFRAME_HASH_TO_DISPLAY_ID[df_hash] = display_id

    df_name = get_df_variable_name(
        df,
        ipython_shell=ipython_shell,
        df_hash=df_hash,
    )
    DATAFRAME_HASH_TO_VAR_NAME[df_hash] = df_name
    logger.debug(f"registering display_id {display_id=} for `{df_name}`")
    return f"{df_name}__{df_hash}"


def get_display_id(df_hash: str) -> str:
    """
    Checks whether `df` is a subset of any others currently being tracked,
    and either returns the known display ID or creates a new one.
    """
    if df_hash in SUBSET_TO_DATAFRAME_HASH:
        parent_df_hash = SUBSET_TO_DATAFRAME_HASH[df_hash]
        display_id = DATAFRAME_HASH_TO_DISPLAY_ID[parent_df_hash]
    else:
        display_id = str(uuid.uuid4())
    return display_id


def store_in_sqlite(table_name: str, df: pd.DataFrame):
    logger.debug(f"{df.columns=}")
    tracking_df = df.copy()

    logger.debug("-- cleaning before sqlite --")
    for col in tracking_df.columns:
        tracking_df[col] = clean_column_values_for_sqlite(tracking_df[col])

    logger.debug(f"writing to `{table_name}` table in sqlite")
    with sql_engine.begin() as conn:
        num_written_rows = tracking_df.to_sql(
            table_name,
            con=conn,
            if_exists="replace",
            index=True,  # this is the default, but just to be explicit
        )
    logger.debug(f"wrote {num_written_rows} row(s) to `{table_name}` table")
    return num_written_rows


def track_column_conversions(
    orig_df: pd.DataFrame,
    df: pd.DataFrame,
    display_id: str,
) -> None:
    # keep track of any original->cleaned column conversions
    # because once the cleaned versions are sent to the frontend,
    # any frontend interactions are going to be referencing values
    # that aren't actually present in the dataset.
    # this means that in filtering.py, we need to apply filters
    # to the cleaned version of the dataframe, pull the index values
    # of the resulting row(s), then swap out the results with the
    # index positions of the original data
    logger.debug(f"{orig_df.columns=}")
    logger.debug(f"{df.columns=}")

    DISPLAY_ID_TO_INDEX[display_id] = df.index.name
    DISPLAY_ID_TO_DATETIME_COLUMNS[display_id] = [
        c for c in orig_df.columns if is_datetime_series(df[c]) and not has_numeric_strings(df[c])
    ]
    DISPLAY_ID_TO_SEQUENCE_COLUMNS[display_id] = [
        c for c in orig_df.columns if is_sequence_series(df[c])
    ]

    if display_id not in DISPLAY_ID_TO_CONVERTED_COLUMNS:
        DISPLAY_ID_TO_CONVERTED_COLUMNS[display_id] = {}

    for col in orig_df.columns:
        if col not in df.columns:
            # hopefully it was set as an index?
            continue

        if df[col].dtype != orig_df[col].dtype:
            DISPLAY_ID_TO_CONVERTED_COLUMNS[display_id][col] = (orig_df[col], df[col])
            continue
        if not (df[col] == orig_df[col]).all():
            DISPLAY_ID_TO_CONVERTED_COLUMNS[display_id][col] = (orig_df[col], df[col])
            continue
