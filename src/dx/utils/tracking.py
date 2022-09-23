import hashlib
import uuid
from typing import List, Optional

import pandas as pd
import structlog
from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell
from pandas.util import hash_pandas_object
from sqlalchemy import create_engine

from dx.settings import get_settings
from dx.utils.datatypes import has_numeric_strings, is_sequence_series
from dx.utils.date_time import is_datetime_series
from dx.utils.formatting import generate_metadata, is_default_index, normalize_index_and_columns

logger = structlog.get_logger(__name__)
sql_engine = create_engine("sqlite://", echo=False)
settings = get_settings()


# should be (display_id: DXDataFrame) pairs
DXDF_CACHE = {}
# not currently used -- will be needed to disambiguate subsets across different cells
CELL_ID_TO_DISPLAY_ID = {}
# used to track when a filtered subset should be tied to an existing display ID
SUBSET_TO_DISPLAY_ID = {}


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
        self.sequence_columns = [column for column in df.columns if is_sequence_series(df[column])]
        self.datetime_columns = [
            c for c in df.columns if is_datetime_series(df[c]) and not has_numeric_strings(df[c])
        ]

        self.default_index_used = is_default_index(df.index)
        self.index_name = df.index.name or "index"

        self.df = normalize_index_and_columns(df)
        self.hash = generate_df_hash(self.df)
        self.sql_table = f"{self.variable_name}_{self.hash}"
        self.display_id = SUBSET_TO_DISPLAY_ID.get(self.hash, str(uuid.uuid4()))

        self.metadata = generate_metadata(self.display_id)
        self.metadata["datalink"]["dataframe_info"] = {
            "default_index_used": self.default_index_used,
            **get_df_dimensions(self.df, prefix="orig"),
        }

    def __repr__(self):
        attr_str = " ".join(
            f"{k}={v}" for k, v in self.__dict__.items() if not isinstance(v, (pd.DataFrame))
        )
        return f"<DXDataFrame {attr_str}>"


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
