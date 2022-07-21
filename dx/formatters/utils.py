import sys

import pandas as pd

from dx.formatters.callouts import display_callout
from dx.settings import settings
from dx.types import DXSamplingMode


def human_readable_size(size_bytes: int) -> str:
    size_str = ""
    for unit in ["B", "KiB", "MiB", "GiB", "TiB"]:
        if abs(size_bytes) < 1024.0:
            size_str = f"{size_bytes:3.1f} {unit}"
            break
        size_bytes /= 1024.0
    return size_str


def truncate_if_too_big(
    df: pd.DataFrame,
    orig_num_rows: int = 0,
) -> pd.DataFrame:
    """
    Reduces the length of a dataframe if it is too big,
    to help reduce size of data being sent to the frontend
    for non-default media types.
    """
    max_size_bytes = settings.MAX_RENDER_SIZE_BYTES
    if sys.getsizeof(df) > max_size_bytes:
        num_current_rows = len(df)
        num_rows_to_remove = int(num_current_rows * settings.TRUNCATION_FACTOR)
        num_truncated_rows = num_current_rows - num_rows_to_remove

        truncated_rows = sample(df, num_truncated_rows)

        size = num_current_rows
        if orig_num_rows > 0:
            # don't overwrite original size if it was
            # established during a previous call
            size = orig_num_rows

        return truncate_if_too_big(truncated_rows, size)

    if orig_num_rows:
        size_string = human_readable_size(max_size_bytes)
        warning_html = f"""Dataframe is bigger than
         <code>{settings.MAX_RENDER_SIZE_BYTES=}</code> ({size_string}),
         so a truncated version is being displayed for DEX (shortened from
         <code>{orig_num_rows:,}</code> to <code>{len(df):,}</code> row(s)).
        """
        display_callout(warning_html, level="warning")

    return df


def sample(df: pd.DataFrame, num_rows: int) -> pd.DataFrame:
    """
    Samples a dataframe to a specified number of rows
    based on Settings.SAMPLING_MODE.
    """
    if settings.SAMPLING_MODE == DXSamplingMode.random:
        return df.sample(num_rows)
    if settings.SAMPLING_MODE == DXSamplingMode.first:
        return df.head(num_rows)
    if settings.SAMPLING_MODE == DXSamplingMode.last:
        return df.tail(num_rows)
    raise ValueError(f"Unknown sampling mode: {settings.SAMPLING_MODE}")
