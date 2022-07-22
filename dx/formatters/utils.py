import sys

import pandas as pd

from dx.formatters.callouts import display_callout
from dx.settings import settings
from dx.types import DXSamplingMethod


def human_readable_size(size_bytes: int) -> str:
    size_str = ""
    for unit in ["B", "KiB", "MiB", "GiB", "TiB"]:
        if abs(size_bytes) < 1024.0:
            size_str = f"{size_bytes:3.1f} {unit}"
            break
        size_bytes /= 1024.0
    return size_str


def truncate_if_too_big(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reduces the size of a dataframe if it is too big,
    to help reduce the amount of data being sent to the
    frontend for non-default media types.
    """
    warnings = []

    # check number of columns first, then trim rows if needed
    max_columns = settings.DISPLAY_MAX_COLUMNS
    df_too_wide = len(df.columns) > max_columns
    if df_too_wide:
        num_orig_columns = len(df.columns)
        df = sample_columns(df, max_columns)
        col_warning = f"""Dataframe has {num_orig_columns:,} column(s),
         which is more than <code>{settings.DISPLAY_MAX_COLUMNS=}</code>"""
        warnings.append(col_warning)

    # check number of rows next, then start reducing even more
    max_rows = settings.DISPLAY_MAX_ROWS
    df_too_long = len(df) > max_rows
    if df_too_long:
        num_orig_rows = len(df)
        df = sample_rows(df, max_rows)
        row_warning = f"""Dataframe has {num_orig_rows:,} row(s),
         which is more than <code>{settings.DISPLAY_MAX_ROWS=}</code>"""
        warnings.append(row_warning)

    # in the event that there are nested/large values bloating the dataframe,
    # easiest to reduce rows even further here
    max_size_bytes = settings.MAX_RENDER_SIZE_BYTES
    df_too_big = sys.getsizeof(df) > max_size_bytes
    if df_too_big:
        orig_size = sys.getsizeof(df)
        df = reduce_df(df)
        size_str = human_readable_size(orig_size)
        max_size_str = human_readable_size(max_size_bytes)
        settings_size_str = (
            f"<code>{settings.MAX_RENDER_SIZE_BYTES=}</code> ({max_size_str})"
        )
        size_warning = (
            f"""Dataframe is {size_str}, which is more than {settings_size_str}"""
        )
        warnings.append(size_warning)

    if warnings:
        warning_html = "<br/>".join(warnings)
        new_size_html = f"""A truncated version with <strong>{len(df):,}</code> row(s) and
         {len(df.reset_index().columns):,} column(s)</strong> will be viewable in DEX."""
        warning_html = f"{warning_html}<br/>{new_size_html}"
        display_callout(warning_html, level="warning")

    return df


def reduce_df(df: pd.DataFrame, orig_num_rows: int = 0) -> pd.DataFrame:
    """
    May recursively reduce the number of rows in a dataframe,
    depending on MAX_RENDER_SIZE_BYTES.
    (Reserved for dataframes with large values but acceptable
    row/column counts.)
    """
    if sys.getsizeof(df) <= settings.MAX_RENDER_SIZE_BYTES:
        return df

    num_current_rows = len(df)
    num_rows_to_remove = int(num_current_rows * settings.TRUNCATION_FACTOR)
    num_truncated_rows = num_current_rows - num_rows_to_remove
    truncated_rows = sample_rows(df, num_truncated_rows)

    size = num_current_rows
    if orig_num_rows > 0:
        # don't overwrite original size if it was
        # established during a previous call
        size = orig_num_rows

    return reduce_df(truncated_rows, size)


def sample_columns(df: pd.DataFrame, num_cols: int) -> pd.DataFrame:
    """
    Samples a dataframe to a specified number of rows
    based on Settings.SAMPLING_METHOD.
    """
    sampling = settings.SAMPLING_METHOD
    if col_sampling := settings.COLUMN_SAMPLING_METHOD != sampling:
        sampling = col_sampling

    # transposing here to treat columns like rows to take advantage of
    # pandas' .head()/.tail()/.sample(), which are row-oriented operations
    # which we can then transpose back to original column orientation
    if sampling == DXSamplingMethod.random:
        return sample_random(df.transpose(), num_cols).transpose()
    if sampling == DXSamplingMethod.first:
        return sample_first(df.transpose(), num_cols).transpose()
    if sampling == DXSamplingMethod.last:
        return sample_last(df.transpose(), num_cols).transpose()
    if sampling == DXSamplingMethod.inner:
        return sample_inner(df.transpose(), num_cols).transpose()
    if sampling == DXSamplingMethod.outer:
        return sample_outer(df.transpose(), num_cols).transpose()

    raise ValueError(f"Unknown sampling method: {sampling}")


def sample_rows(df: pd.DataFrame, num_rows: int) -> pd.DataFrame:
    """
    Samples a dataframe to a specified number of rows
    based on Settings.SAMPLING_METHOD.
    """
    sampling = settings.SAMPLING_METHOD
    if row_sampling := settings.ROW_SAMPLING_METHOD != sampling:
        sampling = row_sampling

    if sampling == DXSamplingMethod.random:
        return sample_random(df, num_rows)
    if sampling == DXSamplingMethod.first:
        return sample_first(df, num_rows)
    if sampling == DXSamplingMethod.last:
        return sample_last(df, num_rows)
    if sampling == DXSamplingMethod.inner:
        return sample_inner(df, num_rows)
    if sampling == DXSamplingMethod.outer:
        return sample_outer(df, num_rows)

    raise ValueError(f"Unknown sampling method: {sampling}")


def sample_first(df: pd.DataFrame, num: int) -> pd.DataFrame:
    """
    Samples the first N rows.

    Example: sampling first 8 of 20 rows:
    [XXXXXXXX............]
    """
    return df.head(num)


def sample_last(df: pd.DataFrame, num: int) -> pd.DataFrame:
    """
    Samples the last N rows.

    Example: sampling last 8 of 20 rows:
    [............XXXXXXXX]
    """
    return df.tail(num)


def sample_random(df: pd.DataFrame, num: int) -> pd.DataFrame:
    """
    Samples a random selection of N rows based on the RANDOM_STATE seed.

    Example: sampling random 8 of 20 rows:
    [XX...XX.X..X...X.XX.]
    """
    return df.sample(num, random_state=settings.RANDOM_STATE)


def sample_inner(df: pd.DataFrame, num: int) -> pd.DataFrame:
    """
    Samples the inner N rows.

    Example: sampling inner 8 of 20 rows:
    [......XXXXXXXX......]
    """
    # rounding down since we'll be adding one filler row
    # as well as using the index
    middle_index = int(len(df) / 2) - 1
    inner_buffer = int(num / 2)
    middle_start = middle_index - inner_buffer
    middle_end = middle_index + inner_buffer
    return df.iloc[middle_start:middle_end, :]


def sample_outer(df: pd.DataFrame, num: int) -> pd.DataFrame:
    """
    Samples the outer N rows.

    Example: sampling outer 8 of 20 rows:
    [XXXX............XXXX]
    """
    # rounding down since we'll be adding one filler row
    # as well as using the index
    outer_buffer = int(num / 2) - 1
    start_rows = df.head(outer_buffer)

    # hack to make a column/row filled with ellipsis values
    # to show hidden data between outer rows
    buffer_col = df.head(1).transpose()
    buffer_col.columns = ["..."]
    buffer_col["..."] = "..."
    buffer_row = buffer_col.transpose()

    end_rows = df.tail(outer_buffer)
    return pd.concat([start_rows, buffer_row, end_rows])


def stringify_columns(df: pd.DataFrame) -> pd.DataFrame:
    cols = df.columns

    def stringify_multiindex(vals):
        return ", ".join(map(str, vals))

    if isinstance(cols, pd.MultiIndex):
        cols = cols.map(stringify_multiindex)
    else:
        cols = cols.map(str)

    df.columns = cols
    return df


def stringify_indices(df: pd.DataFrame) -> pd.DataFrame:
    return stringify_columns(df.transpose()).transpose()
