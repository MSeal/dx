import hashlib
import logging
import os
import sys
import warnings
from functools import lru_cache
from typing import Optional

import pandas as pd
from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell
from IPython.display import update_display
from pandas.util import hash_pandas_object
from pydantic import BaseSettings, Field

from dx.config import DEFAULT_IPYTHON_DISPLAY_FORMATTER, IN_IPYTHON_ENV
from dx.formatters.callouts import display_callout
from dx.settings import settings

logging.basicConfig(
    level=logging.DEBUG,
    force=True,
    stream=sys.stdout,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

warnings.filterwarnings("ignore")


# TODO: make some more structured cache to handle all of this
CELLID_TO_DISPLAY_IDS = {}
DATAFRAME_HASH_TO_DISPLAY_ID = {}
DATAFRAME_HASH_TO_VAR_NAME = {}
DISPLAY_ID_TO_COLUMNS = {}
DISPLAY_ID_TO_DATAFRAME_HASH = {}


class PandasSettings(BaseSettings):
    # "default" (pandas) display mode
    PANDAS_DISPLAY_MAX_ROWS: int = 60
    PANDAS_DISPLAY_MAX_COLUMNS: int = 20
    PANDAS_HTML_TABLE_SCHEMA: bool = Field(False, allow_mutation=False)
    PANDAS_MEDIA_TYPE: str = Field("application/vnd.dataresource+json", allow_mutation=False)

    class Config:
        validate_assignment = True  # we need this to enforce `allow_mutation`


@lru_cache
def get_pandas_settings():
    return PandasSettings()


pandas_settings = get_pandas_settings()


def reset(ipython_shell: Optional[InteractiveShell] = None) -> None:
    """
    Resets all nteract/Noteable options, reverting to the default
    pandas display options and IPython display formatter.
    """
    if not IN_IPYTHON_ENV and ipython_shell is None:
        return

    global settings
    settings.DISPLAY_MODE = "default"

    settings.DISPLAY_MAX_COLUMNS = pandas_settings.PANDAS_DISPLAY_MAX_COLUMNS
    settings.DISPLAY_MAX_ROWS = pandas_settings.PANDAS_DISPLAY_MAX_ROWS
    settings.MEDIA_TYPE = pandas_settings.PANDAS_MEDIA_TYPE

    pd.set_option("display.max_columns", pandas_settings.PANDAS_DISPLAY_MAX_COLUMNS)
    pd.set_option("display.max_rows", pandas_settings.PANDAS_DISPLAY_MAX_ROWS)

    ipython = ipython_shell or get_ipython()
    ipython.display_formatter = DEFAULT_IPYTHON_DISPLAY_FORMATTER


def _filter_and_update_display(
    cell_id: str,
    filter: str,
    output_variable_name: Optional[str] = None,
) -> None:
    """
    Filters the dataframe in the cell with the given cell_id.
    """
    display_id = get_display_id_for_cell(cell_id)
    df_hash = DISPLAY_ID_TO_DATAFRAME_HASH[display_id]

    # update DEX
    df = pd.read_parquet(f"/tmp/{df_hash}.parquet", engine="pyarrow")
    columns = DISPLAY_ID_TO_COLUMNS[display_id]
    df.columns = columns

    # TODO: fix issues with .query where the columns aren't strings
    df.columns = _string_flatten_columns(df.columns)

    df_name = DATAFRAME_HASH_TO_VAR_NAME[df_hash]
    logger.debug(f"applying filter to `{df_name=}`: {filter=}")
    new_df = df.query(filter, engine="python")
    logger.debug(f"updating {display_id=} with {new_df.shape=}")
    update_display(new_df, display_id=display_id)

    # update callout
    callout_display_id = display_id + "-primary"
    output_variable_name = output_variable_name or "new_df"
    filter_code = f"""{output_variable_name} = {df_name}.query({filter}, engine="python")"""
    logger.debug(f"updating callout display for {callout_display_id=} ->\n{filter_code=}")
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


def get_display_id_for_cell(cell_id: str) -> str:
    display_ids = CELLID_TO_DISPLAY_IDS[cell_id]
    if not display_ids:
        raise ValueError(f"{cell_id=} -> {CELLID_TO_DISPLAY_IDS=}")
    return display_ids[-1]


def get_display_id_for_df(df: pd.DataFrame) -> str:
    df_hash = _generate_df_hash(df)
    return DATAFRAME_HASH_TO_DISPLAY_ID[df_hash]


def _generate_df_hash(df: pd.DataFrame) -> str:
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


def _get_df_variable_name(
    df: pd.DataFrame,
    ipython_shell: Optional[InteractiveShell] = None,
) -> str:
    """
    Returns the variable name of the DataFrame object.
    """
    ipython = ipython_shell or get_ipython()
    df_vars = {k: v for k, v in ipython.user_ns.items() if isinstance(v, pd.DataFrame)}
    logger.debug(f"dataframe variables present: {list(df_vars.keys())}")
    for name, obj in df_vars.items():
        if str(name).startswith("_"):
            # ignore _, __, ___, etc.
            # TODO: handle when a dataset is rendered without variable assignment
            continue
        if _generate_df_hash(obj) == _generate_df_hash(df):
            return name


def _register_display_id(
    df: pd.DataFrame,
    display_id: str,
) -> None:
    global CELLID_TO_DISPLAY_IDS
    global DATAFRAME_HASH_TO_DISPLAY_ID
    global DATAFRAME_HASH_TO_VAR_NAME
    global DISPLAY_ID_TO_DATAFRAME_HASH
    global DISPLAY_ID_TO_COLUMNS

    cell_id = get_cell_id()
    cell_display_ids = CELLID_TO_DISPLAY_IDS.get(cell_id, [])
    cell_display_ids.append(display_id)
    CELLID_TO_DISPLAY_IDS[cell_id] = cell_display_ids

    df_hash = _generate_df_hash(df)
    DISPLAY_ID_TO_DATAFRAME_HASH[display_id] = df_hash
    DATAFRAME_HASH_TO_DISPLAY_ID[df_hash] = display_id

    df_name = _get_df_variable_name(df)
    DATAFRAME_HASH_TO_VAR_NAME[df_hash] = df_name

    # parquet needs string columns, which could cause problems for multi-index columns
    DISPLAY_ID_TO_COLUMNS[display_id] = df.columns
    df.columns = _string_flatten_columns(df.columns)
    df.to_parquet(f"/tmp/{df_hash}.parquet", engine="pyarrow")


def _string_flatten_columns(columns: pd.Series) -> pd.Series:
    if isinstance(columns, pd.MultiIndex):
        columns = columns.to_flat_index()
    return columns.astype(str)
