from typing import Optional

import pandas as pd
import structlog

from dx.datatypes import date_time, geometry, misc, numeric
from dx.settings import settings
from dx.types.dex_metadata import DEXMetadata, DEXView

logger = structlog.get_logger(__name__)


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

    df = pd.DataFrame(obj)
    return df


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
    display_df = df.copy()

    display_df = normalize_index(display_df)
    display_df = normalize_columns(display_df)
    display_df = deconflict_index_and_column_names(display_df)

    return display_df


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
        standard_dtypes = ["float", "int", "bool"]
        if df[column].dtype in standard_dtypes or str(df[column].dtype).startswith("datetime"):
            logger.debug(f"skipping `{column=}` since it has dtype `{df[column].dtype}`")
            continue
        logger.debug(f"--> cleaning `{column=}` with dtype `{df[column].dtype}`")
        df[column] = clean_column_values(df[column])
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


def clean_column_values(s: pd.Series) -> pd.Series:
    """
    Cleaning/conversion for values in a series to prevent
    build_table_schema() or frontend rendering errors.
    """
    s = date_time.handle_time_period_series(s)
    s = date_time.handle_time_delta_series(s)
    s = date_time.handle_date_series(s)

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
    extra_metadata: Optional[dict] = None,
    **dataframe_info,
):
    from dx.utils.tracking import DXDF_CACHE

    filters = []
    sample_history = []
    dex_metadata = DEXMetadata()

    # pull the topmost-parent dataframe's metadata, if available
    if (parent_dxdf := DXDF_CACHE.get(display_id)) is not None:
        existing_metadata = parent_dxdf.metadata
        parent_dataframe_info = existing_metadata.get("datalink", {}).get("dataframe_info", {})
        dex_metadata = DEXMetadata.parse_obj(existing_metadata.get("dx", {}))
        logger.info(f"existing {dex_metadata=}")
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
        filters = [dex_filter.dict() for dex_filter in parent_dxdf.filters]

    if not dex_metadata.views:
        logger.info("no views found, adding default view")
        dex_metadata.add_view(
            variable_name=variable_name,
            display_id=display_id,
        )

    # user-defined extra metadata overrides
    dex_metadata = handle_extra_metadata(
        dex_metadata,
        variable_name,
        df.attrs,
    )

    # metadata called from other convenience functions
    dex_metadata = handle_extra_metadata(
        dex_metadata,
        variable_name,
        extra_metadata,
    )

    metadata = {
        "datalink": {
            "dataframe_info": dataframe_info,
            "dx_settings": settings.dict(
                exclude={
                    "RENDERABLE_OBJECTS": True,
                    "DATETIME_STRING_FORMAT": True,
                    "MEDIA_TYPE": True,
                }
            ),
            "display_id": display_id,
            "applied_filters": filters,
            "sample_history": sample_history,
            "sampling_time": pd.Timestamp("now").strftime(settings.DATETIME_STRING_FORMAT),
            "variable_name": variable_name,
        },
        "dx": dex_metadata.dict(by_alias=True),
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


def handle_extra_metadata(
    metadata: DEXMetadata,
    variable_name: str,
    extra_metadata: dict,
) -> DEXMetadata:
    if not extra_metadata:
        return metadata

    # determine whether extra_metadata belongs to the top-level metadata
    # or if it needs to be matched to a view
    try:
        if is_dex_view_metadata(extra_metadata):
            metadata = update_dex_view_metadata(metadata, variable_name, extra_metadata)
        elif is_dex_metadata(extra_metadata):
            metadata = update_dex_metadata(metadata, extra_metadata)
        else:
            logger.warning(f"not sure what to do with {extra_metadata=}")
    except Exception as e:
        logger.info(f'error updating metadata: "{e}"')
    logger.info(f"done handling extra metadata, {metadata=}")
    return metadata


def update_dex_view_metadata(
    metadata: DEXMetadata,
    variable_name: str,
    extra_metadata: dict,
) -> DEXMetadata:
    # ensure original variable name is carried through
    # if it isn't explicitly set
    if "variable_name" not in extra_metadata:
        extra_metadata["variable_name"] = variable_name

    # assume the user wants this update to be shown
    if "is_default" not in extra_metadata:
        extra_metadata["is_default"] = True

    # TODO: what if the variable matches more than one view?
    updated_views = []
    updated_existing_view = False
    for view in metadata.views:
        # disable other views from being shown by default
        view = view.copy(update={"is_default": False})
        if not updated_existing_view and view.variable_name == variable_name:
            logger.info(f"updating {view.display_id=} with {extra_metadata=}")
            view = view.copy(update=extra_metadata)
            updated_existing_view = True
        updated_views.append(view)

    if not updated_existing_view:
        logger.info(f"didn't match to existing view; adding new view with {extra_metadata=}")
        metadata.add_view(**extra_metadata)
    else:
        metadata.views = updated_views

    return metadata


def update_dex_metadata(metadata: DEXMetadata, extra_metadata: dict) -> DEXMetadata:
    logger.info(f"updating metadata with {extra_metadata=}")
    return metadata.copy(update=extra_metadata)


def is_dex_metadata(metadata: dict) -> bool:
    new_metadata_keys = set(metadata.keys())
    dex_metadata_keys = set(DEXMetadata().dict().keys())
    dex_metadata_alias_keys = set(DEXMetadata().dict(by_alias=True).keys())
    return bool(new_metadata_keys & (dex_metadata_keys | dex_metadata_alias_keys))


def is_dex_view_metadata(metadata: dict) -> bool:
    new_metadata_keys = set(metadata.keys())
    dex_view_metadata_keys = set(DEXView().dict().keys())
    dex_view_metadata_alias_keys = set(DEXView().dict(by_alias=True).keys())
    return bool(new_metadata_keys & (dex_view_metadata_keys | dex_view_metadata_alias_keys))


def clean_pandas_query_column(column: str) -> str:
    """
    Converts column names into a more pandas .query()-friendly format.
    """
    # pandas will raise errors if the columns are numeric
    # e.g. "UndefinedVariableError: name 'BACKTICK_QUOTED_STRING_{column}' is not defined"
    # so we have to refer to them as pd.Series object using `@df[column]` structure
    # except we don't know the name of the variable here, so we pass {df_name} as a placeholder
    # to be filled in by the kernel*
    # ---
    # *as of August 2022, the dx package is using this for Datalink processing and filling df_name
    # as part of its internal tracking
    if str(column).isdigit() or str(column).isdecimal():
        return f"@{{df_name}}[{column}]"
    return f"`{column}`"
