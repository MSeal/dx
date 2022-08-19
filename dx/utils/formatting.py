import numpy as np
import pandas as pd
import structlog

from dx.settings import settings
from dx.utils import datatypes, date_time, geometry

logger = structlog.get_logger(__name__)


def human_readable_size(size_bytes: int) -> str:
    """
    Converts bytes to a more human-readable string.

    >>> human_readable_size(1689445298)
    '1.5 GiB'
    """
    size_str = ""
    for unit in ["B", "KiB", "MiB", "GiB", "TiB"]:
        if abs(size_bytes) < 1024.0:
            size_str = f"{size_bytes:3.1f} {unit}"
            break
        size_bytes /= 1024.0
    return size_str


def is_default_index(index: pd.Index) -> bool:
    """
    Returns True if the index values are 0-n, where n is the number of items in the series.
    """
    index_vals = index.values.tolist()
    default_index = pd.Index(list(range(len(index_vals))))
    index = pd.Index(sorted(index_vals))
    return index.equals(default_index)


def normalize_index_and_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Any additional formatting that needs to happen to the index,
    the columns, or the data itself should be done here.
    """
    display_df = df.copy()

    if settings.RESET_INDEX_VALUES and not is_default_index(display_df.index):
        # preserve 0-n row numbers for frontend
        # if custom/MultiIndex is used
        display_df.reset_index(inplace=True)

    # if index or column values are numeric, we need to convert to strings
    # (whether pd.Index or pd.MultiIndex) to avoid build_table_schema() errors
    logger.debug(f"before: {display_df.index[:5]=}")
    if settings.STRINGIFY_INDEX_VALUES:
        if isinstance(display_df.index, pd.MultiIndex):
            display_df.index = pd.MultiIndex.from_tuples(
                stringify_index(display_df.index),
                names=list(map(str, display_df.index.names)),
            )
        else:
            display_df.index = pd.Index(
                stringify_index(display_df.index),
                name=str(display_df.index.name),
            )
    if settings.FLATTEN_INDEX_VALUES:
        display_df.index = flatten_index(display_df.index)
    logger.debug(f"after: {display_df.index[:5]=}")

    logger.debug(f"before: {display_df.columns[:5]=}")
    if settings.STRINGIFY_COLUMN_VALUES:
        display_df.columns = pd.Index(stringify_index(display_df.columns))
    if settings.FLATTEN_COLUMN_VALUES:
        display_df.columns = flatten_index(display_df.columns)
    logger.debug(f"after: {display_df.columns[:5]=}")

    # build_table_schema() doesn't like pd.NAs
    display_df.fillna(np.nan, inplace=True)

    for column in display_df.columns:
        display_df[column] = clean_column_values(display_df[column])

    return display_df


def flatten_index(index: pd.Index, separator: str = ", "):
    if not isinstance(index[0], (list, tuple)):
        return index
    return list(map(separator.join, index))


def stringify_index(index: pd.Index):
    """
    Convenience method to cast index/column values as strings.
    (Handles pd.Index as well as pd.MultiIndex objects)
    """
    if isinstance(index[0], (list, tuple)):
        # pd.MultiIndex
        return list(map(stringify_index, index))
    return tuple(map(str, index))


def clean_column_values(s: pd.Series) -> pd.Series:
    """
    Cleaning/conversion for values in a series to prevent
    build_table_schema() or frontend rendering errors.
    """
    s = date_time.handle_time_period_series(s)
    s = date_time.handle_time_delta_series(s)

    s = datatypes.handle_dtype_series(s)
    s = datatypes.handle_interval_series(s)

    s = geometry.handle_geometry_series(s)

    return s
