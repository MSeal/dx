import hashlib
import uuid
from typing import Dict, List, Optional

import pandas as pd
import structlog
from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell
from pandas.util import hash_pandas_object
from sqlalchemy import create_engine

from dx.utils.datatypes import has_numeric_strings, is_sequence_series
from dx.utils.date_time import is_datetime_series
from dx.utils.formatting import generate_metadata, is_default_index, normalize_index_and_columns

logger = structlog.get_logger(__name__)
sql_engine = create_engine("sqlite://", echo=False)


class DXDataFrameCache:
    """
    Convenience class to store information about dataframes,
    including original size, series data types, and other
    dx-generated information such as display_id and hash.
    """

    df: pd.DataFrame = None
    original_column_dtypes: dict = {}
    index: List[str] = []

    id: uuid.UUID = None
    parent_id: uuid.UUID = None

    hash: str = None
    display_id: uuid.UUID = None
    variable_name: str = None

    metadata: dict = {}
    filters: List[dict] = []

    def __init__(self, df: pd.DataFrame):
        from dx.sampling import get_df_dimensions

        self.original_column_dtypes = df.dtypes.to_dict()
        self.sequence_columns = [column for column in df.columns if is_sequence_series(df[column])]
        self.datetime_columns = [
            c for c in df.columns if is_datetime_series(df[c]) and not has_numeric_strings(df[c])
        ]

        self.default_index_used = is_default_index(df.index)
        self.index_name = df.index.name or "index"

        self.id = uuid.uuid4()
        self.df = normalize_index_and_columns(df)

        self.hash = generate_df_hash(self.df)
        self.variable_name = get_df_variable_name(self.df, df_hash=self.hash)
        self.sql_table = f"{self.variable_name}_{self.hash}"
        self.display_id = get_display_id(self.hash)

        self.metadata = generate_metadata(self.display_id)
        self.metadata["datalink"]["dataframe_info"] = get_df_dimensions(self.df, prefix="orig")

    def __repr__(self):
        attr_str = " ".join(
            f"{k}={v}" for k, v in self.__dict__.items() if not isinstance(v, (pd.DataFrame))
        )
        return f"<DXDataFrameCache {attr_str}>"


class DXCacheManager:
    """
    Convenience class for keeping track of DXDataFrameCache
    objects, to include convenience methods for getting a DXDataFrameCache
    by display_id or by variable name.
    """

    dataframe_caches: List[DXDataFrameCache] = []
    filter_subsets: Dict[str, DXDataFrameCache] = {}

    def __repr__(self):
        return f"<DXCacheManager {len(self.dataframe_caches)} cache(s)>"

    def add(self, df: pd.DataFrame):
        dfc = DXDataFrameCache(df)
        self.dataframe_caches.append(dfc)

    def get_by_display_id(self, display_id: str) -> DXDataFrameCache:
        return next(dfc for dfc in self.dataframe_caches if dfc.display_id == display_id)


cache_manager = DXCacheManager()


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
    df_hash: Optional[str] = None,
) -> str:
    """
    Returns the variable name of the DataFrame object.
    """
    logger.debug("looking for matching variables for dataframe")

    ipython = ipython_shell or get_ipython()
    df_vars = {k: v for k, v in ipython.user_ns.items() if isinstance(v, pd.DataFrame)}
    logger.debug(f"dataframe variables present: {list(df_vars.keys())}")

    df_hash = df_hash or generate_df_hash(df)
    matching_df_vars = []
    for k, v in df_vars.items():
        logger.debug(f"checking if `{k}` is equal to this dataframe")
        # we previously checked columns, dtypes, shape, etc between both dataframes,
        # to avoid having to normalize and hash the other dataframe (v here),
        # but that was too slow, and ultimately we shouldn't be checking raw data vs cleaned data
        # so <df>.equals(<other_df>) should be the most performant
        if df.equals(v):
            logger.debug(f"`{k}` matches this dataframe")
            matching_df_vars.append(k)
    logger.debug(f"dataframe variables with same hash: {matching_df_vars}")

    # we might get a mix of references here like ['_', '__', 'df']
    named_df_vars_with_same_hash = [name for name in matching_df_vars if not name.startswith("_")]
    logger.debug(f"named dataframe variables with same hash: {named_df_vars_with_same_hash}")
    if named_df_vars_with_same_hash:
        logger.debug(f"{named_df_vars_with_same_hash=}")
        return named_df_vars_with_same_hash[-1]

    if matching_df_vars:
        # dataframe rendered without variable assignment
        logger.debug(f"no matching dataframe variables found: {matching_df_vars=}")
        return matching_df_vars[-1]

    # no dataframe variables found, assign a new one for internal referencing
    logger.debug("no variables found matching this dataframe")
    df_uuid = f"unk_dataframe_{uuid.uuid4()}".replace("-", "")
    return df_uuid


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
