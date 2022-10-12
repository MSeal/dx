import pandas as pd
import structlog

from dx.settings import settings
from dx.utils import datatypes, date_time, geometry

logger = structlog.get_logger(__name__)


def is_default_index(index: pd.Index) -> bool:
    """
    Returns True if the index have no specified name,
    are of `int` type, and are a pd.Index (instead of pd.MultiIndex).
    """
    if isinstance(index, pd.MultiIndex):
        return False

    if index.dtype != "int":
        return False

    if index.name is not None:
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

    s = datatypes.handle_dtype_series(s)
    s = datatypes.handle_interval_series(s)
    s = datatypes.handle_ip_address_series(s)
    s = datatypes.handle_complex_number_series(s)

    s = geometry.handle_geometry_series(s)

    s = datatypes.handle_dict_series(s)
    s = datatypes.handle_sequence_series(s)
    s = datatypes.handle_unk_type_series(s)
    return s


def generate_metadata(display_id: str, default_index_used: bool = True, **dataframe_info):
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
        filters = [dex_filter.dict() for dex_filter in parent_dxdf.filters]

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
        },
        "display_id": display_id,
    }
    logger.debug(f"{metadata=}")
    return metadata
