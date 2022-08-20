import hashlib
import json
import uuid
from typing import Optional

import pandas as pd
import structlog
from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell
from pandas.util import hash_pandas_object
from sqlalchemy import create_engine

from dx.utils.formatting import clean_column_values, flatten_sequences
from dx.utils.geometry import handle_geometry_series

logger = structlog.get_logger(__name__)
sql_engine = create_engine("sqlite://", echo=False)


DATAFRAME_HASH_TO_DISPLAY_ID = {}
DATAFRAME_HASH_TO_VAR_NAME = {}
DISPLAY_ID_TO_COLUMNS = {}
DISPLAY_ID_TO_DATAFRAME_HASH = {}
SUBSET_TO_DATAFRAME_HASH = {}


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
    hash_df = df.copy()

    # some dtypes can't be hashed
    for col in hash_df.columns:
        hash_df[col] = hash_df[col].apply(flatten_sequences)
        hash_df[col] = handle_geometry_series(hash_df[col])
        hash_df[col] = hash_df[col].apply(lambda x: json.dumps(x) if isinstance(x, dict) else x)

    # this will be a series of hash values the length of df
    df_hash_series = hash_pandas_object(hash_df)
    # then string-concatenate all the hashed values, which could be very large
    df_hash_str = "-".join(df_hash_series.astype(str))
    # then hash the resulting (potentially large) string
    hash_str = hashlib.sha256(df_hash_str.encode()).hexdigest()
    return hash_str


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
    is_subset: bool = False,
    ipython_shell: Optional[InteractiveShell] = None,
) -> None:
    """
    Hashes the dataframe object and tracks display_id for future references in other function calls,
    and writes the data to a local sqlite table for follow-on SQL querying.
    """

    if is_subset:
        logger.debug("rendered subset of original dataset; not re-registering")
        return

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
    return f"{df_name}__{df_hash}"


def get_display_id(df: pd.DataFrame) -> str:
    """
    Checks whether `df` is a subset of any others currently being tracked,
    and either returns the known display ID or creates a new one.
    """
    df_obj = pd.DataFrame(df)
    df_obj_hash = generate_df_hash(df_obj)
    if df_obj_hash in SUBSET_TO_DATAFRAME_HASH:
        parent_df_hash = SUBSET_TO_DATAFRAME_HASH[df_obj_hash]
        parent_df_name = DATAFRAME_HASH_TO_VAR_NAME[parent_df_hash]
        display_id = DATAFRAME_HASH_TO_DISPLAY_ID[parent_df_hash]
        logger.debug(f"rendering subset of original dataframe '{parent_df_name}'")
    else:
        display_id = str(uuid.uuid4())
    return display_id


def df_is_subset(df: pd.DataFrame) -> bool:
    """
    Determines whether or not a dataframe has already been associated
    with a parent dataframe during a filter/update call.
    """
    df_hash = generate_df_hash(df)
    is_subset = df_hash in SUBSET_TO_DATAFRAME_HASH
    logger.debug(f"{df_hash=} {is_subset=}")
    return is_subset


def store_in_sqlite(table_name: str, df: pd.DataFrame):
    tracking_df = df.copy()

    # make sure any dtypes/geometries/etc are converted
    for column in tracking_df.columns:
        tracking_df[column] = clean_column_values(tracking_df[column])

        # flatten any lists/sets/tuples
        tracking_df[column] = tracking_df[column].apply(flatten_sequences)
        tracking_df[column] = tracking_df[column].apply(
            lambda x: json.dumps(x) if isinstance(x, dict) else x
        )

    logger.debug(f"writing to `{table_name}` table in sqlite")
    with sql_engine.begin() as conn:
        num_written_rows = tracking_df.to_sql(table_name, con=conn, if_exists="replace")
    logger.debug(f"wrote {num_written_rows} row(s) to `{table_name}` table")
