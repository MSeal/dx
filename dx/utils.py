import uuid

import numpy as np
import pandas as pd

from dx.config import GEOPANDAS_INSTALLED
from dx.filtering import (
    DATAFRAME_HASH_TO_DISPLAY_ID,
    DATAFRAME_HASH_TO_VAR_NAME,
    SUBSET_FILTERS,
    SUBSET_TO_DATAFRAME_HASH,
    generate_df_hash,
    register_display_id,
)
from dx.loggers import get_logger
from dx.sampling import stringify_columns

logger = get_logger(__name__)


def human_readable_size(size_bytes: int) -> str:
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

    # preserve 0-n row numbers for frontend
    # if custom/MultiIndex is used
    if not is_default_index(display_df.index):
        display_df.reset_index(inplace=True)

    # temporary workaround for numeric column rendering errors with GRID
    # https://noteables.slack.com/archives/C03CB8A4Z2L/p1658497348488939
    display_df = stringify_columns(display_df)

    # build_table_schema() doesn't like pd.NAs
    display_df.fillna(np.nan, inplace=True)

    for column in display_df.columns:
        display_df[column] = handle_column_dtypes(display_df[column])

    return display_df


def series_has_types(s: pd.Series, types: tuple) -> bool:
    return any(isinstance(v, types) for v in s.values)


def handle_column_dtypes(s: pd.Series) -> pd.Series:
    types = (type, np.dtype)
    if series_has_types(s, types):
        logger.debug(f"{s.name} has types; converting to strings")
        s = s.astype(str)

    if GEOPANDAS_INSTALLED:
        import geopandas as gpd
        import shapely.geometry.base

        geometry_types = (
            shapely.geometry.base.BaseGeometry,
            shapely.geometry.base.BaseMultipartGeometry,
        )
        if series_has_types(s, geometry_types):
            logger.debug(f"{s.name} has geometries; converting to JSON")
            s = gpd.GeoSeries(s).to_json()

    return s


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
        register_display_id(df_obj.copy(), display_id)
    return display_id


def get_applied_filters(df: pd.DataFrame) -> dict:
    """
    Returns a dictionary of applied filters for a dataframe.
    """
    df_hash = generate_df_hash(df)
    return SUBSET_FILTERS[df_hash]


def df_is_subset(df: pd.DataFrame) -> bool:
    """
    Determines whether or not a dataframe has already been associated
    with a parent dataframe during a filter/update call.
    """
    df_hash = generate_df_hash(df)
    return df_hash in SUBSET_TO_DATAFRAME_HASH
