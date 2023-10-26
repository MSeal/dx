from typing import Iterable

import pandas as pd
import structlog

from dx.datatypes import date_time, geometry, misc, numeric
from dx.settings import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()


def to_dataframe(obj) -> pd.DataFrame:
    """
    Converts an object to a pandas dataframe.
    """
    logger.debug(f"converting {type(obj)} to pd.DataFrame")

    # handling for groupby operations returning pd.Series
    index_reset_name = None
    if is_groupby_series(obj):
        orig_index_names = obj.index.names
        index_reset_name = groupby_series_index_name(obj.index)
        # this will convert a MultiIndex series to a flat DataFrame
        obj = obj.reset_index(name=index_reset_name)
        # ensure we keep the original index structure
        obj.set_index(orig_index_names, inplace=True)

    # special handling for non-pandas objects
    # if we can't cast directly to a DataFrame
    for dtype, converter in settings.get_renderable_types().items():
        if isinstance(obj, dtype) and converter is not None:
            if isinstance(converter, str):
                # class method
                conversion_method = getattr(obj, converter)
                df = conversion_method()
                break
            elif callable(converter):
                # function
                df = converter(obj)
                break
    else:
        df = pd.DataFrame(obj)

    return df


def incrementing_label(value: str, iter: Iterable) -> str:
    """
    Returns a string with an incrementing suffix if the value
    already exists in the iterable.
    """
    suffix = 1
    while f"{value}_{suffix}" in iter:
        suffix += 1
    return f"{value}_{suffix}"


def check_for_duplicate_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handles duplicate columns by appending an incrementing suffix
    to the column name.
    """
    if not df.columns.duplicated().any():
        return df

    dupes = pd.Series(df.columns.duplicated(), index=df.columns)
    # filtering to any that are True
    dupes = dupes[dupes]
    # counting the number of duplicates per column to warn the user
    logger.warning(f"duplicate columns found: {dupes.groupby(dupes.index).sum().to_dict()}")

    new_df = pd.DataFrame()
    for col_num, column in enumerate(df.columns):
        if column in new_df.columns:
            if isinstance(column, tuple):
                # flatten it since it will be flattened later anyway
                column = ",".join([str(x) for x in column])
            column = incrementing_label(column, new_df.columns)
        new_df[column] = df.iloc[:, col_num]

    new_df.index = df.index
    return new_df


def is_groupby_series(s: pd.Series) -> bool:
    """
    Checks if the pd.Series is the result of a groupby operation
    by checking if the index is a MultiIndex and its name is
    also used as a level in its index.

    Example:

    df = pd.DataFrame({
        'foo': list('aaabbcddee'),
        'bar': np.random.rand(1, 10)[0],
        'baz': np.random.randint(-10, 10, 10)
    })

    group = df.groupby('foo').bar.value_counts()
    print(group)
    >>> foo  bar
    a    0.304653    1
         0.440604    1
         0.445702    1
    b    0.164294    1
         0.296721    1
    c    0.789996    1
    d    0.550120    1
         0.948220    1
    e    0.223248    1
         0.664756    1
    Name: bar, dtype: int64

    print(group.index.names)
    >>> ['foo', 'bar']

    print(group.name)
    >>> bar
    """
    if not isinstance(s, pd.Series):
        return False
    if not isinstance(s.index, pd.MultiIndex):
        return False
    return s.name in s.index.names


def groupby_series_index_name(index: pd.MultiIndex) -> str:
    """
    Creates a name for groupby operations to provide using a .reset_index()
    based on the dataframe's MultiIndex names.

    Example:
    - A MultiIndex with level names of ["foo", "bar"] will return "foo.bar.value"
    """
    index_trail = ".".join([str(name) for name in index.names])
    return f"{index_trail}.value"


def is_default_index(index: pd.Index) -> bool:
    """
    Returns True if the index have no specified name,
    are of `int` type, are a pd.Index (instead of pd.MultiIndex),
    and are unique.
    """
    if isinstance(index, pd.MultiIndex):
        return False

    if index.dtype != "int":
        return False

    if index.name is not None:
        return False

    if not index.is_unique:
        # if DataFrames with default indexes are concatenated,
        # we may pass every check above, but have duplicate
        # index values
        return False

    # we aren't checking for 0-n row values because any kind of
    # filtering or sampling will create gaps and incorrectly
    # mark this as a non-default index (return False)
    return True


def normalize_index_and_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Any additional formatting that needs to happen to the index,
    the columns, or the data itself should be done here.
    """
    df = normalize_index(df)
    df = normalize_columns(df)
    df = deconflict_index_and_column_names(df)
    return df


def normalize_index(df: pd.DataFrame) -> pd.DataFrame:
    """ """
    if settings.RESET_INDEX_VALUES and not is_default_index(df.index):
        # preserve 0-n row numbers for frontend
        # if custom/MultiIndex is used
        df.reset_index(inplace=True)

    is_multiindex = isinstance(df.index, pd.MultiIndex)

    # if index or column values are numeric, we need to convert to strings
    # (whether pd.Index or pd.MultiIndex) to avoid build_table_schema() errors
    index_name = getattr(df.index, "names", None)
    # may be `FrozenList([None, None ...])`
    if not any(index_name):
        index_name = getattr(df.index, "name")
    index_name = index_name or "index"
    # build_table_schema() doesn't like non-string index names
    if not isinstance(index_name, str):
        if is_multiindex:
            index_name = list(map(str, index_name))
        else:
            index_name = str(index_name)

    if settings.FLATTEN_INDEX_VALUES and is_multiindex:
        df.index = df.index.to_flat_index()
        df.index = [", ".join([str(val) for val in index_vals]) for index_vals in df.index]

    if settings.STRINGIFY_INDEX_VALUES:
        if is_multiindex:
            df.index = pd.MultiIndex.from_tuples(stringify_index(df.index), names=index_name)
        else:
            df.index = pd.Index(stringify_index(df.index), name=index_name)

    # also ensure we clean for any unrenderable types - casting to pd.Series because various Index
    # types don't have `.head()` methods
    if not is_multiindex:
        df.index = clean_series_values(pd.Series(df.index))
    else:
        clean_levels = []
        for level in df.index.levels:
            clean_level = clean_series_values(pd.Series(level))
            clean_levels.append(clean_level)
        df.index.set_levels(clean_levels, level=index_name, inplace=True)

    return df


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Any additional formatting that needs to happen to the columns,
    or the data itself should be done here.
    """
    if settings.FLATTEN_COLUMN_VALUES and isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.to_flat_index()
        df.columns = [", ".join([str(val) for val in column_vals]) for column_vals in df.columns]

    if settings.STRINGIFY_COLUMN_VALUES:
        df.columns = pd.Index(stringify_index(df.columns))

    logger.debug("-- cleaning columns before display --")
    for column in df.columns:
        df[column] = clean_series_values(df[column])
    return df


def stringify_index(index: pd.Index):
    """
    Convenience method to cast index/column values as strings.
    (Handles pd.Index as well as pd.MultiIndex objects)
    """
    if isinstance(index[0], (list, tuple)):
        # pd.MultiIndex
        return list(map(stringify_index, index))
    return tuple(map(str, index))


def clean_series_values(s: pd.Series) -> pd.Series:
    """
    Cleaning/conversion for values in a series to prevent build_table_schema(), display(), or
    frontend rendering errors.
    """
    dtype_str = str(s.dtype)

    if dtype_str in {"float", "int", "bool"}:
        # skip standard dtypes
        logger.debug(f"skipping `{s.name}` since it has dtype `{dtype_str}`")
        return s

    if dtype_str.startswith("datetime") and not dtype_str.startswith("datetime64[ns, "):
        # skip datetime series that are not tz-aware datetime64[ns, <tz>]
        # because we need to handle some minor adjustments for tz information before build_table_schema()
        logger.debug(f"skipping `{s.name}` since it has dtype `{dtype_str}`")
        return s

    logger.debug(f"--> cleaning `{s.name}` with dtype `{dtype_str}`")

    s = date_time.handle_time_period_series(s)
    s = date_time.handle_time_delta_series(s)
    s = date_time.handle_datetime_series(s)

    s = numeric.handle_decimal_series(s)
    s = numeric.handle_complex_number_series(s)

    s = misc.handle_dtype_series(s)
    s = misc.handle_interval_series(s)
    s = misc.handle_ip_address_series(s)

    s = geometry.handle_geometry_series(s)

    s = misc.handle_dict_series(s)
    s = misc.handle_sequence_series(s)
    s = misc.handle_unk_type_series(s)
    return s


def generate_metadata(
    df: pd.DataFrame,
    display_id: str,
    variable_name: str = "",
    **dataframe_info,
):
    from dx.utils.tracking import DXDF_CACHE

    filters = []
    sample_history = []

    # pull the topmost-parent dataframe's metadata, if available
    if (parent_dxdf := DXDF_CACHE.get(display_id)) is not None:
        existing_metadata = parent_dxdf.metadata
        parent_dataframe_info = existing_metadata.get("datalink", {}).get("dataframe_info", {})
        if parent_dataframe_info:
            # if this comes after a resampling operation, we need to make sure the
            # original dimensions aren't overwritten by this new dataframe_info,
            # but instead we want to update the previous dataframe_info with the
            # updated values for the truncated* dimensions
            # (`truncated_size_bytes`, `truncated_num_rows`, `truncated_num_cols`)
            truncated_dataframe_info = {
                k: v for k, v in dataframe_info.items() if k.startswith("truncated")
            }
            parent_dataframe_info.update(truncated_dataframe_info)
            dataframe_info = parent_dataframe_info
        # these are set whenever store_sample_to_history() is called after a filter action from the frontend
        sample_history = existing_metadata.get("datalink", {}).get("sample_history", [])
        # we shouldn't have a mix of pydantic FilterTypes and dicts here, but just in case
        filters = [f.dict() if not isinstance(f, dict) else f for f in parent_dxdf.filters]

    # TODO: wrap this up into the DXDataFrame init properties with some refactoring
    user_variable_name = variable_name
    if str(variable_name).startswith("unk_dataframe_") and len(variable_name) == 46:
        # `unk_dataframe_<hash>` with dashes removed, which is what we use
        # to reference dataframe objects not explicitly assigned to variables
        # where we need to keep a reference to them in duckdb without relying on
        # temporary variables in the user namespace
        user_variable_name = None

    metadata = {
        "datalink": {
            "dataframe_info": dataframe_info,
            "dx_settings": settings.dict(
                exclude={
                    "RENDERABLE_TYPES": True,
                    "DATETIME_STRING_FORMAT": True,
                    "MEDIA_TYPE": True,
                }
            ),
            "display_id": display_id,
            "applied_filters": filters,
            "sample_history": sample_history,
            "sampling_time": pd.Timestamp("now").strftime(settings.DATETIME_STRING_FORMAT),
            "variable_name": variable_name,
            "user_variable_name": user_variable_name,
        },
        "display_id": display_id,
    }

    logger.debug(f"{metadata=}")
    return metadata


def deconflict_index_and_column_names(df: pd.DataFrame) -> pd.DataFrame:
    # we may encounter dataframes that contain the same
    # column and index name(s), which will cause problems
    # during .reset_index() later, so we need to rename
    # the columns to keep the index structure the same
    index_names = set([df.index.name])
    if isinstance(df.index, pd.MultiIndex):
        index_names = set(df.index.names)

    column_names = set(df.columns)
    intersecting_names = column_names.intersection(index_names)
    if not intersecting_names:
        return df

    logger.debug(f"handling columns found in index names: {intersecting_names}")
    column_renames = {column: f"{column}.value" for column in intersecting_names}
    return df.rename(columns=column_renames)


def get_default_thresholds(s: pd.Series, bins: int = 5):
    cuts = pd.cut(s, bins)
    thresholds = [t.right for t in cuts.cat.categories[:-1]]
    return thresholds
