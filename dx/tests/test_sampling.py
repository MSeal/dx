import sys

import pandas as pd

from dx.sampling import sample_if_too_big
from dx.settings import get_settings, settings_context

settings = get_settings()


def test_small_dataframe_is_not_sampled(sample_dataframe: pd.DataFrame):
    """
    Test that a small dataframe is not sampled.
    """
    original_size_bytes = sys.getsizeof(sample_dataframe)
    sampled_df = sample_if_too_big(sample_dataframe)
    sampled_size_bytes = sys.getsizeof(sampled_df)
    assert sampled_size_bytes <= settings.MAX_RENDER_SIZE_BYTES
    assert sampled_size_bytes == original_size_bytes


def test_large_dataframe_is_sampled(sample_large_dataframe: pd.DataFrame):
    """
    Test that a large dataframe is sampled to below the size of
    MAX_RENDER_SIZE_BYTES.
    """
    with settings_context(
        MAX_RENDER_SIZE_BYTES=1024 * 1024,
        DISPLAY_MAX_ROWS=100,
        DISPLAY_MAX_COLUMNS=100,
    ):
        original_size_bytes = sys.getsizeof(sample_large_dataframe)
        sampled_df = sample_if_too_big(sample_large_dataframe)
        sampled_size_bytes = sys.getsizeof(sampled_df)
        assert sampled_size_bytes <= settings.MAX_RENDER_SIZE_BYTES
        assert sampled_size_bytes < original_size_bytes


def test_sampled_dataframe_keeps_dtypes(sample_large_dataframe: pd.DataFrame):
    """
    Test that a sampled dataframe doesn't alter column datatypes.
    """
    with settings_context(
        MAX_RENDER_SIZE_BYTES=1024 * 1024,
        DISPLAY_MAX_ROWS=100,
        DISPLAY_MAX_COLUMNS=100,
    ):
        orig_dtypes = sample_large_dataframe.dtypes
        sampled_df = sample_if_too_big(sample_large_dataframe)
        assert (sampled_df.dtypes == orig_dtypes).all()


def test_wide_dataframe_is_narrowed(sample_wide_dataframe: pd.DataFrame):
    """
    Test that a wide dataframe is narrowed to below the size of
    the display mode's MAX_COLUMNS setting.
    """
    orig_width = len(sample_wide_dataframe.columns)
    narrow_df = sample_if_too_big(sample_wide_dataframe)
    narrow_width = len(narrow_df.columns)
    assert narrow_width < orig_width, f"{narrow_width=}"
    assert narrow_width <= settings.DISPLAY_MAX_COLUMNS


def test_long_dataframe_is_shortened(sample_long_dataframe: pd.DataFrame):
    """
    Test that a long dataframe is shortened to below the size of
    the display mode's MAX_ROWS setting.
    """
    orig_length = len(sample_long_dataframe)
    short_df = sample_if_too_big(sample_long_dataframe)
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
    reduced_df = sample_if_too_big(sample_long_wide_dataframe)
    reduced_width = len(reduced_df.columns)
    reduced_length = len(reduced_df)
    assert reduced_width < orig_width
    assert reduced_width <= settings.DISPLAY_MAX_COLUMNS
    assert reduced_length < orig_length
    assert reduced_length <= settings.DISPLAY_MAX_ROWS
