import sys

import pandas as pd

from dx.formatters.utils import is_default_index, normalize_index_and_columns, truncate_if_too_big
from dx.settings import get_settings

settings = get_settings()


def test_small_dataframe_is_not_truncated(sample_dataframe: pd.DataFrame):
    """
    Test that a small dataframe is not truncated.
    """
    original_size_bytes = sys.getsizeof(sample_dataframe)
    truncated_df = truncate_if_too_big(sample_dataframe)
    truncated_size_bytes = sys.getsizeof(truncated_df)
    assert truncated_size_bytes <= settings.MAX_RENDER_SIZE_BYTES
    assert truncated_size_bytes == original_size_bytes


def test_large_dataframe_is_truncated(sample_large_dataframe: pd.DataFrame):
    """
    Test that a large dataframe is truncated to below the size of
    MAX_RENDER_SIZE_BYTES.
    """
    original_size_bytes = sys.getsizeof(sample_large_dataframe)
    truncated_df = truncate_if_too_big(sample_large_dataframe)
    truncated_size_bytes = sys.getsizeof(truncated_df)
    assert truncated_size_bytes <= settings.MAX_RENDER_SIZE_BYTES
    assert truncated_size_bytes < original_size_bytes


def test_truncated_dataframe_keeps_dtypes(sample_large_dataframe: pd.DataFrame):
    """
    Test that a truncated dataframe doesn't alter column datatypes.
    """
    orig_dtypes = sample_large_dataframe.dtypes
    truncated_df = truncate_if_too_big(sample_large_dataframe)
    assert (truncated_df.dtypes == orig_dtypes).all()


def test_wide_dataframe_is_narrowed(sample_wide_dataframe: pd.DataFrame):
    """
    Test that a wide dataframe is narrowed to below the size of
    the display mode's MAX_COLUMNS setting.
    """
    orig_width = len(sample_wide_dataframe.columns)
    narrow_df = truncate_if_too_big(sample_wide_dataframe)
    narrow_width = len(narrow_df.columns)
    assert narrow_width < orig_width, f"{narrow_width=}"
    assert narrow_width <= settings.DISPLAY_MAX_COLUMNS


def test_long_dataframe_is_shortened(sample_long_dataframe: pd.DataFrame):
    """
    Test that a long dataframe is shortened to below the size of
    the display mode's MAX_ROWS setting.
    """
    orig_length = len(sample_long_dataframe)
    short_df = truncate_if_too_big(sample_long_dataframe)
    short_length = len(short_df)
    assert short_length < orig_length, f"{short_length=}"
    assert short_length <= settings.DISPLAY_MAX_ROWS


def test_long_wide_dataframe_is_reduced_from_both_dimensions(
    sample_long_wide_dataframe: pd.DataFrame,
):
    """
    Test that a long wide dataframe is reduced from both dimensions
    to below the size of the display mode's MAX_COLUMNS and MAX_ROWS settings.
    """
    orig_width = len(sample_long_wide_dataframe.columns)
    orig_length = len(sample_long_wide_dataframe)
    reduced_df = truncate_if_too_big(sample_long_wide_dataframe)
    reduced_width = len(reduced_df.columns)
    reduced_length = len(reduced_df)
    assert reduced_width < orig_width
    assert reduced_width <= settings.DISPLAY_MAX_COLUMNS
    assert reduced_length < orig_length
    assert reduced_length <= settings.DISPLAY_MAX_ROWS


def test_default_index_returns_true(sample_dataframe: pd.DataFrame):
    index = sample_dataframe.index
    assert is_default_index(index)


def test_custom_index_returns_false(sample_dataframe: pd.DataFrame):
    sample_dataframe.set_index("col_1", inplace=True)
    index = sample_dataframe.index
    assert not is_default_index(index)


def test_multiindex_returns_false(sample_dataframe: pd.DataFrame):
    sample_dataframe.set_index(["col_1", "col_2"], inplace=True)
    index = sample_dataframe.index
    assert not is_default_index(index)


def test_default_index_persists(sample_dataframe: pd.DataFrame):
    """
    Default indexes should not be reset.
    """
    df = normalize_index_and_columns(sample_dataframe.copy())
    assert df.index.equals(sample_dataframe.index)


def test_custom_index_resets(sample_dataframe: pd.DataFrame):
    """
    Custom indexes should reset to ensure the `index` is passed
    with row value numbers to the frontend, from 0 to the length of the dataframe.
    """
    sample_dataframe.set_index(["col_1", "col_2"], inplace=True)
    df = normalize_index_and_columns(sample_dataframe.copy())
    assert not df.index.equals(sample_dataframe.index)
