import sys

from dx.config import DEFAULT_MAX_SIZE_BYTES
from dx.formatters.utils import truncate_if_too_big


def test_small_dataframe_is_not_truncated(sample_dataframe):
    """
    Test that a small dataframe is not truncated.
    """
    original_size_bytes = sys.getsizeof(sample_dataframe)
    truncated_df = truncate_if_too_big(sample_dataframe)
    truncated_size_bytes = sys.getsizeof(truncated_df)
    assert truncated_size_bytes == original_size_bytes
    assert truncated_size_bytes <= DEFAULT_MAX_SIZE_BYTES


def test_large_dataframe_is_truncated(sample_large_dataframe):
    """
    Test that a large dataframe is truncated to below the size of
    DEFAULT_MAX_SIZE_BYTES.
    """
    original_size_bytes = sys.getsizeof(sample_large_dataframe)
    truncated_df = truncate_if_too_big(sample_large_dataframe)
    truncated_size_bytes = sys.getsizeof(truncated_df)
    assert truncated_size_bytes < original_size_bytes
    assert truncated_size_bytes <= DEFAULT_MAX_SIZE_BYTES
