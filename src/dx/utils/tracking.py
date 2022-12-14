import hashlib
import os
import uuid
from functools import lru_cache
from typing import List, Optional, Union

import duckdb
import pandas as pd
import structlog
from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell
from pandas.util import hash_pandas_object

from dx.settings import get_settings
from dx.utils.formatting import generate_metadata, is_default_index, normalize_index_and_columns

logger = structlog.get_logger(__name__)
settings = get_settings()


# should be (display_id: DXDataFrame) pairs
DXDF_CACHE = {}
# used to track when a filtered subset should be tied to an existing display ID
SUBSET_HASH_TO_PARENT_DATA = {}


@lru_cache
def get_db_connection() -> duckdb.DuckDBPyConnection:
    return duckdb.connect(database=settings.DB_LOCATION, read_only=False)


class DXDataFrame:
    """
    Convenience class to store information about dataframes,
    including original size, series data types, and other
    dx-generated information such as display_id and hash.
    """

    df: pd.DataFrame = None
    original_column_dtypes: dict = {}
    index_name: List[str] = []

    id: uuid.UUID = None
    parent_id: uuid.UUID = None

    hash: str = None
    display_id: uuid.UUID = None
    variable_name: str = None

    metadata: dict = {}
    filters: List[dict] = []

    def __init__(
        self,
        df: pd.DataFrame,
        ipython_shell: Optional[InteractiveShell] = None,
    ):
        from dx.sampling import get_df_dimensions

        self.id = uuid.uuid4()
        self.variable_name = get_df_variable_name(df, ipython_shell=ipython_shell)

        self.original_column_dtypes = df.dtypes.to_dict()

        self.default_index_used = is_default_index(df.index)
        self.index_name = get_df_index(df.index)

        self.df = normalize_index_and_columns(df)
        self.hash = generate_df_hash(self.df)

        self.cell_id = self.get_cell_id()
        self.display_id = self.get_display_id()

        self.metadata: dict = generate_metadata(
            df=self.df,
            display_id=self.display_id,
            variable_name=self.variable_name,
        )
        self.metadata["datalink"]["dataframe_info"] = {
            "default_index_used": self.default_index_used,
            **get_df_dimensions(self.df, prefix="orig"),
        }

    def __repr__(self):
        attr_str = " ".join(
            f"{k}={v}" for k, v in self.__dict__.items() if not isinstance(v, (pd.DataFrame))
        )
        return f"<DXDataFrame {attr_str}>"

    def get_cell_id(self) -> str:
        last_executed_cell_id = os.environ.get("LAST_EXECUTED_CELL_ID")
        cell_id = SUBSET_HASH_TO_PARENT_DATA.get(self.hash, {}).get(
            "cell_id", last_executed_cell_id
        )
        logger.debug(f"DXDF {last_executed_cell_id=} / last associated {cell_id=}")
        return cell_id

    def get_display_id(self) -> str:
        display_id = SUBSET_HASH_TO_PARENT_DATA.get(self.hash, {}).get(
            "display_id", str(uuid.uuid4())
        )
        logger.debug(f"DXDF {display_id=}")
        return display_id


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
    # this will be a series of hash values the length of df
    df_hash_series = hash_pandas_object(df)
    # then string-concatenate all the hashed values, which could be very large
    df_hash_str = "-".join(df_hash_series.astype(str))
    # then hash the resulting (potentially large) string
    hash_str = hashlib.sha256(df_hash_str.encode()).hexdigest()
    return hash_str


def get_df_index(index: Union[pd.Index, pd.MultiIndex]):
    index_name = index.name
    if index_name is None and isinstance(index, pd.MultiIndex):
        index_name = index.names
    if index_name is None:
        # no custom index was used, but will be set to `index`
        # before storing in the database, which we'll need to
        # reset after any database querying
        index_name = "index"
    return index_name


def get_df_variable_name(
    df: pd.DataFrame,
    ipython_shell: Optional[InteractiveShell] = None,
) -> str:
    """
    Returns the variable name of the DataFrame object
    by inspecting the IPython shell's user namespace
    and comparing `df` to the available variables and their values.
    """
    logger.debug("looking for matching variables for dataframe")

    ipython = ipython_shell or get_ipython()
    df_vars = {
        k: v
        for k, v in ipython.user_ns.items()
        if isinstance(v, tuple(settings.RENDERABLE_OBJECTS))
    }
    logger.debug(f"dataframe variables present: {list(df_vars.keys())}")

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
    logger.debug(f"dataframe variables with same data: {matching_df_vars}")

    # we might get a mix of references here like ['_', '__', 'df']
    named_df_vars_with_same_data = [name for name in matching_df_vars if not name.startswith("_")]
    logger.debug(f"named dataframe variables with same hash: {named_df_vars_with_same_data}")
    if named_df_vars_with_same_data:
        logger.debug(f"{named_df_vars_with_same_data=}")
        return named_df_vars_with_same_data[0]

    if matching_df_vars:
        # dataframe rendered without variable assignment
        logger.debug(f"no matching dataframe variables found: {matching_df_vars=}")
        return matching_df_vars[-1]

    # no dataframe variables found, assign a new one for internal referencing
    logger.debug("no variables found matching this dataframe")
    df_uuid = f"unk_dataframe_{uuid.uuid4()}".replace("-", "")
    return df_uuid
