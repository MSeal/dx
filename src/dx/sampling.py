import sys
from typing import Optional

import numpy as np
import pandas as pd
import structlog

from dx.settings import settings
from dx.types.main import DXSamplingMethod

logger = structlog.get_logger(__name__)


def sample_if_too_big(df: pd.DataFrame, display_id: Optional[str] = None) -> pd.DataFrame:
    """
    Reduces the size of a dataframe if it is too big,
    to help reduce the amount of data being sent to the
    frontend for non-default media types.
    """
    orig_dtypes = set(df.dtypes.to_dict().items())

    # check number of columns first, then trim rows if needed
    max_columns = settings.DISPLAY_MAX_COLUMNS
    df_too_wide = len(df.columns) > max_columns
    if df_too_wide:
        df = sample_columns(df, num_cols=max_columns)

    # check number of rows next, then start reducing even more
    max_rows = settings.DISPLAY_MAX_ROWS
    df_too_long = len(df) > max_rows
    if df_too_long:
        df = sample_rows(df, num_rows=max_rows, display_id=display_id)

    # in the event that there are nested/large values bloating the dataframe,
    # easiest to reduce rows even further here
    max_size_bytes = settings.MAX_RENDER_SIZE_BYTES
    df_too_big = sys.getsizeof(df) > max_size_bytes
    if df_too_big:
        df = reduce_df(df)

    # sampling may convert columns to `object` dtype, so we need to make sure
    # the original dtypes persist before generating the body for the frontend
    current_dtypes = set(df.dtypes.to_dict())
    dtype_conversions = orig_dtypes - current_dtypes
    if dtype_conversions:
        for column, dtype in dtype_conversions:
            if column not in df.columns:
                # this is a column that was dropped during sampling
                logger.debug(f"`{column}` no longer in df, skipping dtype conversion")
                continue
            if str(df[column].dtype) == str(dtype):
                continue
            logger.debug(f"converting `{column}` from `{df[column].dtype!r}` to `{dtype!r}`")
            df[column] = df[column].astype(dtype)

    return df


def reduce_df(df: pd.DataFrame, orig_num_rows: int = 0) -> pd.DataFrame:
    """
    May recursively reduce the number of rows in a dataframe,
    depending on MAX_RENDER_SIZE_BYTES.
    (Reserved for dataframes with large values but acceptable
    row/column counts.)
    """
    if sys.getsizeof(df) <= settings.MAX_RENDER_SIZE_BYTES:
        return df

    num_current_rows = len(df)
    num_rows_to_remove = int(num_current_rows * settings.SAMPLING_FACTOR)
    num_truncated_rows = num_current_rows - num_rows_to_remove
    truncated_rows = sample_rows(df, num_truncated_rows)

    size = num_current_rows
    if orig_num_rows > 0:
        # don't overwrite original size if it was
        # established during a previous call
        size = orig_num_rows

    return reduce_df(truncated_rows, size)


def sample_columns(df: pd.DataFrame, num_cols: int) -> pd.DataFrame:
    """
    Samples a dataframe to a specified number of rows
    based on Settings.SAMPLING_METHOD, or
    Settings.COLUMN_SAMPLING_METHOD if specified.
    """
    sampling = settings.SAMPLING_METHOD
    if (col_sampling := settings.COLUMN_SAMPLING_METHOD) != sampling:
        sampling = col_sampling

    # transposing here to treat columns like rows to take advantage of
    # pandas' .head()/.tail()/.sample(), which are row-oriented operations
    # which we can then transpose back to original column orientation
    if sampling == DXSamplingMethod.random:
        return sample_random(df.transpose(), num_cols).transpose()
    if sampling == DXSamplingMethod.first:
        return sample_first(df.transpose(), num_cols).transpose()
    if sampling == DXSamplingMethod.last:
        return sample_last(df.transpose(), num_cols).transpose()
    if sampling == DXSamplingMethod.inner:
        return sample_inner(df.transpose(), num_cols).transpose()
    if sampling == DXSamplingMethod.outer:
        return sample_outer(df.transpose(), num_cols).transpose()

    raise ValueError(f"Unknown sampling method: {sampling}")


def sample_rows(df: pd.DataFrame, num_rows: int, display_id: Optional[str] = None) -> pd.DataFrame:
    """
    Samples a dataframe to a specified number of rows
    based on Settings.SAMPLING_METHOD, or
    Settings.ROW_SAMPLING_METHOD if specified.
    """
    sampling = settings.SAMPLING_METHOD
    if (row_sampling := settings.ROW_SAMPLING_METHOD) != sampling:
        sampling = row_sampling

    if sampling == DXSamplingMethod.random:
        return sample_random(df, num_rows, display_id=display_id)
    if sampling == DXSamplingMethod.first:
        return sample_first(df, num_rows)
    if sampling == DXSamplingMethod.last:
        return sample_last(df, num_rows)
    if sampling == DXSamplingMethod.inner:
        return sample_inner(df, num_rows)
    if sampling == DXSamplingMethod.outer:
        return sample_outer(df, num_rows)

    raise ValueError(f"Unknown sampling method: {sampling}")


def sample_first(df: pd.DataFrame, num: int) -> pd.DataFrame:
    """
    Samples the first N rows.

    Example: sampling first 8 of 20 rows:
    [XXXXXXXX............]
    """
    return df.head(num)


def sample_last(df: pd.DataFrame, num: int) -> pd.DataFrame:
    """
    Samples the last N rows.

    Example: sampling last 8 of 20 rows:
    [............XXXXXXXX]
    """
    return df.tail(num)


def sample_random(df: pd.DataFrame, num: int, display_id: Optional[str] = None) -> pd.DataFrame:
    """
    Samples a random selection of N rows based on the RANDOM_STATE seed.

    Example: sampling random 8 of 20 rows:
    [XX...XX.X..X...X.XX.]
    """
    # NOTE: this needs to be handled better once DXDataframeCache is implemented
    # so we aren't looking up and re-cleaning the dataframe columns every time,
    # since that causes unnecessary performance issues.

    # if settings.ENABLE_DATALINK:
    #     display_id = display_id or get_display_id_for_df(df)
    #     display_id_array = [ord(v) for v in str(display_id)]
    #     random_state = np.random.RandomState(seed=display_id_array)
    #     logger.debug(f"using random seed {random_state} from {display_id=}")

    random_state = settings.RANDOM_STATE
    return df.sample(num, random_state=random_state)


def sample_inner(df: pd.DataFrame, num: int) -> pd.DataFrame:
    """
    Samples the inner N rows.

    Example: sampling inner 8 of 20 rows:
    [......XXXXXXXX......]
    """
    middle_index = int(len(df) / 2)
    inner_buffer = int(num / 2)
    middle_start = middle_index - inner_buffer
    middle_end = middle_index + inner_buffer
    return df.iloc[middle_start:middle_end, :]


def sample_outer(df: pd.DataFrame, num: int) -> pd.DataFrame:
    """
    Samples the outer N rows.

    Example: sampling outer 8 of 20 rows:
    [XXXX............XXXX]
    """
    outer_buffer = int(num / 2)
    start_rows = df.head(outer_buffer)
    end_rows = df.tail(outer_buffer)
    return pd.concat([start_rows, end_rows])


def get_df_dimensions(df: pd.DataFrame, prefix: Optional[str] = None) -> dict:
    """
    Returns a dictionary of shape/size information
    about the dataframe.
    """
    if prefix is not None:
        prefix = f"{prefix}_"
    else:
        prefix = ""

    df_bytes_size: pd.Series = df.memory_usage()
    # casting to int to allow json serializing later
    df_total_bytes_size: np.int64 = int(df_bytes_size.sum())

    num_rows, num_cols = df.shape
    return {
        f"{prefix}size_bytes": df_total_bytes_size,
        f"{prefix}num_rows": num_rows,
        f"{prefix}num_cols": num_cols,
    }
