import duckdb
import pandas as pd
import pytest
from IPython.terminal.interactiveshell import TerminalInteractiveShell

from dx.filtering import handle_resample, resample_from_db, store_sample_to_history
from dx.formatters.main import handle_format
from dx.settings import get_settings, settings_context
from dx.types.filters import DEXFilterSettings, DEXResampleMessage
from dx.utils.tracking import DXDF_CACHE, DXDataFrame

settings = get_settings()


@pytest.mark.parametrize("has_filters", [True, False])
def test_store_sample_to_history(
    sample_dxdataframe: DXDataFrame,
    sample_dex_filters: list,
    has_filters: bool,
):
    """
    Test that filters applied during sampling are added to
    the DXDataFrame object's metadata.
    """
    display_id = sample_dxdataframe.display_id
    DXDF_CACHE[display_id] = sample_dxdataframe

    filters = []
    if has_filters:
        filters = sample_dex_filters

    store_sample_to_history(
        sample_dxdataframe.df,
        display_id,
        filters,
    )

    assert sample_dxdataframe.metadata["datalink"]["applied_filters"] == filters
    assert sample_dxdataframe.metadata["datalink"]["sampling_time"] is not None

    assert (
        sample_dxdataframe.metadata["datalink"]["dataframe_info"]["orig_num_rows"]
        == sample_dxdataframe.df.shape[0]
    )
    assert (
        sample_dxdataframe.metadata["datalink"]["dataframe_info"]["orig_num_cols"]
        == sample_dxdataframe.df.shape[1]
    )


@pytest.mark.parametrize("has_filters", [True, False])
@pytest.mark.parametrize("display_mode", ["simple", "enhanced"])
def test_resample_from_db(
    mocker,
    get_ipython: TerminalInteractiveShell,
    sample_random_dataframe: pd.DataFrame,
    sample_db_connection: duckdb.DuckDBPyConnection,
    sample_dex_filters: list,
    display_mode: str,
    has_filters: bool,
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

        filters = []
        if has_filters:
            filters = sample_dex_filters

        resample_msg = DEXResampleMessage(
            display_id=metadata[settings.MEDIA_TYPE]["display_id"],
            filters=filters,
        )
        try:
            handle_resample(
                resample_msg,
                ipython_shell=get_ipython,
            )
        except Exception as e:
            assert False, f"Resample failed with error: {e}"


@pytest.mark.parametrize("has_filters", [True, False])
@pytest.mark.parametrize("display_mode", ["simple", "enhanced"])
def test_resample_groupby_from_db(
    mocker,
    get_ipython: TerminalInteractiveShell,
    sample_groupby_dataframe: pd.DataFrame,
    sample_db_connection: duckdb.DuckDBPyConnection,
    sample_dex_groupby_filters: list,
    display_mode: str,
    has_filters: bool,
):
    """
    Ensure dataframes with pd.MultiIndex index/columns stored in
    the kernel's local database can be resampled with DEX-provided filters.
    """
    get_ipython.user_ns["test_df"] = sample_groupby_dataframe

    mocker.patch("dx.formatters.main.db_connection", sample_db_connection)
    mocker.patch("dx.filtering.db_connection", sample_db_connection)

    with settings_context(enable_datalink=True, display_mode=display_mode):
        _, metadata = handle_format(
            sample_groupby_dataframe,
            ipython_shell=get_ipython,
        )

        filters = []
        if has_filters:
            filters = sample_dex_groupby_filters

        resample_msg = DEXResampleMessage(
            display_id=metadata[settings.MEDIA_TYPE]["display_id"],
            filters=filters,
        )
        try:
            handle_resample(
                resample_msg,
                ipython_shell=get_ipython,
            )
        except Exception as e:
            assert False, f"Resample failed with error: {e}"


@pytest.mark.parametrize("has_filters", [True, False])
@pytest.mark.parametrize("display_mode", ["simple", "enhanced"])
def test_resample_keeps_original_structure(
    mocker,
    get_ipython: TerminalInteractiveShell,
    sample_random_dataframe: pd.DataFrame,
    sample_db_connection: duckdb.DuckDBPyConnection,
    sample_dex_filters: list,
    display_mode: str,
    has_filters: bool,
):
    """
    Ensure resampled dataframes have the same column/index structure
    after resampling as the original dataframe.
    """
    get_ipython.user_ns["test_df"] = sample_random_dataframe

    mocker.patch("dx.formatters.main.db_connection", sample_db_connection)
    mocker.patch("dx.filtering.db_connection", sample_db_connection)

    with settings_context(enable_datalink=True, display_mode=display_mode):
        _, metadata = handle_format(
            sample_random_dataframe,
            ipython_shell=get_ipython,
        )

        sample_size = 50_000
        dex_filters = DEXFilterSettings(filters=sample_dex_filters)
        sql_filter_str = dex_filters.to_sql_query()
        if has_filters:
            sql_filter = f"SELECT * FROM {{table_name}} WHERE {sql_filter_str} LIMIT {sample_size}"
            filters = sample_dex_filters
        else:
            sql_filter = f"SELECT * FROM {{table_name}} LIMIT {sample_size}"
            filters = None

        try:
            resampled_df = resample_from_db(
                display_id=metadata[settings.MEDIA_TYPE]["display_id"],
                sql_filter=sql_filter,
                filters=filters,
                ipython_shell=get_ipython,
            )
        except Exception as e:
            assert False, f"Resample failed with error: {e}"

        # we should never end up with more rows than the original dataframe,
        # but we may get fewer rows depending on the filters applied
        assert resampled_df.shape[0] <= sample_random_dataframe.shape[0]
        # we should never end up with more columns than the original dataframe
        assert resampled_df.shape[1] == sample_random_dataframe.shape[1]
