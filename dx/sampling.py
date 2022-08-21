import sys
from typing import Optional, Tuple

import numpy as np
import pandas as pd
import structlog

from dx.formatters.callouts import display_callout
from dx.settings import settings
from dx.types import DXSamplingMethod
from dx.utils.formatting import human_readable_size
from dx.utils.tracking import get_display_id_for_df

logger = structlog.get_logger(__name__)


def sample_if_too_big(df: pd.DataFrame, display_id: Optional[str] = None) -> pd.DataFrame:
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
        df = sample_columns(df, num_cols=max_columns)
        col_warning = f"""Dataframe has {num_orig_columns:,} column(s),
         which is more than <code>{settings.DISPLAY_MAX_COLUMNS=}</code>"""
        warnings.append(col_warning)

    # check number of rows next, then start reducing even more
    max_rows = settings.DISPLAY_MAX_ROWS
    df_too_long = len(df) > max_rows
    if df_too_long:
        num_orig_rows = len(df)
        df = sample_rows(df, num_rows=max_rows, display_id=display_id)
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
        settings_size_str = f"<code>{settings.MAX_RENDER_SIZE_BYTES=}</code> ({max_size_str})"
        size_warning = f"""Dataframe is {size_str}, which is more than {settings_size_str}"""
        warnings.append(size_warning)

    # TODO: replace with custom callout media type
    if warnings:
        warning_html = "<br/>".join(warnings)
        new_size_html = f"""A truncated version with <strong>{len(df):,}</code> row(s) and
         {len(df.reset_index().columns):,} column(s)</strong> will be viewable in DEX."""
        warning_html = f"{warning_html}<br/>{new_size_html}"

        # give users more information on how to change settings
        override_snippet = (
            """<mark><code>dx.set_option({setting name}, {new value})</code></mark>"""
        )
        sample_override = """<code>dx.set_option("DISPLAY_MAX_ROWS", 250_000)</code>"""
        override_warning = "<small><i><sup>*</sup>Be careful; increasing these limits may negatively impact performance.</i></small>"
        user_feedback = f"""<div style="padding:0.25rem 1rem;">
            <p>To adjust the settings*, execute {override_snippet} in a new cell.
            <br/>For example, to change the maximum number of rows to display to 250,000,
             you could execute the following: {sample_override}</p>
            {override_warning}</div>"""
        user_feedback_collapsed_section = (
            f"""<details><summary>More Information</summary>{user_feedback}</details>"""
        )

        warning_html = f"{warning_html} {user_feedback_collapsed_section}"
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
    num_rows_to_remove = int(num_current_rows * settings.SAMPLING_FACTOR)
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
    based on Settings.SAMPLING_METHOD, or
    Settings.COLUMN_SAMPLING_METHOD if specified.
    """
    sampling = settings.SAMPLING_METHOD
    if (col_sampling := settings.COLUMN_SAMPLING_METHOD) != sampling:
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


def sample_rows(df: pd.DataFrame, num_rows: int, display_id: Optional[str] = None) -> pd.DataFrame:
    """
    Samples a dataframe to a specified number of rows
    based on Settings.SAMPLING_METHOD, or
    Settings.ROW_SAMPLING_METHOD if specified.
    """
    sampling = settings.SAMPLING_METHOD
    if (row_sampling := settings.ROW_SAMPLING_METHOD) != sampling:
        sampling = row_sampling

    if sampling == DXSamplingMethod.random:
        return sample_random(df, num_rows, display_id=display_id)
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


def sample_random(df: pd.DataFrame, num: int, display_id: Optional[str] = None) -> pd.DataFrame:
    """
    Samples a random selection of N rows based on the RANDOM_STATE seed.

    Example: sampling random 8 of 20 rows:
    [XX...XX.X..X...X.XX.]
    """

    # TODO: use hash for seed instead?
    display_id = display_id or get_display_id_for_df(df)
    display_id_array = [ord(v) for v in str(display_id)]
    random_state = np.random.RandomState(seed=display_id_array)
    logger.debug(f"using random seed {random_state} from {display_id=}")
    return df.sample(num, random_state=random_state)


def sample_inner(df: pd.DataFrame, num: int) -> pd.DataFrame:
    """
    Samples the inner N rows.

    Example: sampling inner 8 of 20 rows:
    [......XXXXXXXX......]
    """
    middle_index = int(len(df) / 2)
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
    outer_buffer = int(num / 2)
    start_rows = df.head(outer_buffer)
    end_rows = df.tail(outer_buffer)
    return pd.concat([start_rows, end_rows])


def sample_and_describe(
    df: pd.DataFrame,
    display_id: Optional[str] = None,
) -> Tuple[pd.DataFrame, dict]:
    """
    Reduces the size of the dataframe, if necessary,
    and generates a dictionary of shape/size information
    about the dataframe before/after truncation.
    """
    num_orig_rows, num_orig_cols = df.shape
    orig_size_bytes = sys.getsizeof(df)

    df = sample_if_too_big(df, display_id=display_id)

    num_truncated_rows, num_truncated_cols = df.shape
    truncated_size_bytes = sys.getsizeof(df)

    dataframe_info = {
        "orig_size_bytes": orig_size_bytes,
        "orig_num_rows": num_orig_rows,
        "orig_num_cols": num_orig_cols,
        "truncated_size_bytes": truncated_size_bytes,
        "truncated_num_rows": num_truncated_rows,
        "truncated_num_cols": num_truncated_cols,
    }
    return df, dataframe_info