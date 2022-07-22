import sys

from dx.formatters.utils import truncate_if_too_big
from dx.settings import get_settings

settings = get_settings()


def test_small_dataframe_is_not_truncated(sample_dataframe):
    """
    Test that a small dataframe is not truncated.
    """
    original_size_bytes = sys.getsizeof(sample_dataframe)
    truncated_df = truncate_if_too_big(sample_dataframe)
    truncated_size_bytes = sys.getsizeof(truncated_df)
    assert truncated_size_bytes == original_size_bytes
    assert truncated_size_bytes <= settings.MAX_RENDER_SIZE_BYTES


def test_large_dataframe_is_truncated(sample_large_dataframe):
    """
    Test that a large dataframe is truncated to below the size of
    MAX_RENDER_SIZE_BYTES.
    """
    original_size_bytes = sys.getsizeof(sample_large_dataframe)
    truncated_df = truncate_if_too_big(sample_large_dataframe)
    truncated_size_bytes = sys.getsizeof(truncated_df)
    assert truncated_size_bytes < original_size_bytes
    assert truncated_size_bytes <= settings.MAX_RENDER_SIZE_BYTES


def test_wide_dataframe_is_narrowed(sample_wide_dataframe):
    """
    Test that a wide dataframe is narrowed to below the size of
    the display mode's MAX_COLUMNS setting.
    """
    orig_width = len(sample_wide_dataframe.columns)
    narrow_df = truncate_if_too_big(sample_wide_dataframe)
    narrow_width = len(narrow_df.columns)
    assert narrow_width < orig_width
    assert narrow_width < settings.DISPLAY_MAX_COLUMNS


def test_long_dataframe_is_shortened(sample_long_dataframe):
    """
    Test that a long dataframe is shortened to below the size of
    the display mode's MAX_ROWS setting.
    """
    orig_length = len(sample_long_dataframe)
    short_df = truncate_if_too_big(sample_long_dataframe)
    short_length = len(short_df)
    assert short_length < orig_length
    assert short_length <= settings.DISPLAY_MAX_ROWS


def test_long_wide_dataframe_is_reduced_from_both_dimensions(
    sample_long_wide_dataframe,
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
    assert reduced_width < settings.DISPLAY_MAX_COLUMNS
    assert reduced_length < orig_length
    assert reduced_length <= settings.DISPLAY_MAX_ROWS
