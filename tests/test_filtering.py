import duckdb
import pandas as pd
import pytest
from IPython.terminal.interactiveshell import TerminalInteractiveShell

from dx.filtering import handle_resample, store_sample_to_history
from dx.formatters.main import handle_format
from dx.settings import get_settings, settings_context
from dx.types import DEXResampleMessage
from dx.utils.tracking import DXDF_CACHE, DXDataFrame

settings = get_settings()


def test_store_sample_to_history(
    sample_dxdataframe: DXDataFrame,
    sample_dex_filters: list,
):
    """
    Test that filters applied during sampling are added to
    the DXDataFrame object's metadata.
    """
    display_id = sample_dxdataframe.display_id
    DXDF_CACHE[display_id] = sample_dxdataframe

    store_sample_to_history(
        sample_dxdataframe.df,
        display_id,
        sample_dex_filters,
    )

    assert sample_dxdataframe.metadata["datalink"]["applied_filters"] == sample_dex_filters
    assert sample_dxdataframe.metadata["datalink"]["sampling_time"] is not None


@pytest.mark.parametrize("display_mode", ["simple", "enhanced"])
def test_resample_from_db(
    mocker,
    get_ipython: TerminalInteractiveShell,
    sample_random_dataframe: pd.DataFrame,
    sample_db_connection: duckdb.DuckDBPyConnection,
    sample_dex_filters: list,
    display_mode: str,
):
    """
    Ensure dataframes stored in the kernel's local database
    can be resampled with DEX-provided filters.
    """
    get_ipython.user_ns["test_df"] = sample_random_dataframe

    mocker.patch("dx.formatters.main.db_connection", sample_db_connection)
    mocker.patch("dx.filtering.db_connection", sample_db_connection)

    with settings_context(enable_datalink=True, display_mode=display_mode):
        _, metadata = handle_format(
            sample_random_dataframe,
            ipython_shell=get_ipython,
        )

        resample_msg = DEXResampleMessage(
            display_id=metadata[settings.MEDIA_TYPE]["display_id"],
            filters=sample_dex_filters,
            limit=50_000,
            cell_id=None,
        )
        try:
            handle_resample(
                resample_msg,
                ipython_shell=get_ipython,
            )
        except Exception as e:
            assert False, f"Resample failed with error: {e}"


@pytest.mark.parametrize("display_mode", ["simple", "enhanced"])
def test_resample_groupby_from_db(
    mocker,
    get_ipython: TerminalInteractiveShell,
    sample_groupby_dataframe: pd.DataFrame,
    sample_db_connection: duckdb.DuckDBPyConnection,
    sample_dex_groupby_filters: list,
    display_mode: str,
):
    """
    Ensure dataframes stored in the kernel's local database
    can be resampled with DEX-provided filters.
    """
    get_ipython.user_ns["test_df"] = sample_groupby_dataframe

    mocker.patch("dx.formatters.main.db_connection", sample_db_connection)
    mocker.patch("dx.filtering.db_connection", sample_db_connection)

    with settings_context(enable_datalink=True, display_mode=display_mode):
        _, metadata = handle_format(
            sample_groupby_dataframe,
            ipython_shell=get_ipython,
        )

        resample_msg = DEXResampleMessage(
            display_id=metadata[settings.MEDIA_TYPE]["display_id"],
            filters=sample_dex_groupby_filters,
            limit=50_000,
            cell_id=None,
        )
        try:
            handle_resample(
                resample_msg,
                ipython_shell=get_ipython,
            )
        except Exception as e:
            assert False, f"Resample failed with error: {e}"
