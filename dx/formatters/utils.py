import sys

import pandas as pd

from dx.config import DEFAULT_MAX_SIZE_BYTES


def truncate_if_too_big(df: pd.DataFrame, reduction=0.1) -> pd.DataFrame:
    """
    Reduces the length of a dataframe if it is too big,
    to help reduce size of data being sent to the frontend
    for non-default media types.
    """
    df_size_bytes = sys.getsizeof(df)
    if df_size_bytes > DEFAULT_MAX_SIZE_BYTES:

        # TODO: render VDOM type element/warning here
        print(f"{df_size_bytes=} is too big! truncating by {reduction:.0%}...")

        # TODO: add configurable sampling strategy
        num_rows_to_remove = int(len(df) * reduction)
        num_truncated_rows = len(df) - num_rows_to_remove
        return truncate_if_too_big(df.sample(num_truncated_rows))

    return df
