import os
import uuid

import duckdb
import pandas as pd
import pytest
from IPython.terminal.interactiveshell import TerminalInteractiveShell

from dx.filtering import handle_resample, resample_from_db, store_sample_to_history
from dx.formatters.main import handle_format
from dx.settings import get_settings, settings_context
from dx.types.filters import DEXFilterSettings, DEXResampleMessage
from dx.utils.tracking import DXDF_CACHE, SUBSET_HASH_TO_PARENT_DATA, DXDataFrame

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

    datalink_metadata = sample_dxdataframe.metadata["datalink"]

    assert datalink_metadata["applied_filters"] == filters
    if has_filters:
        # ensure sampling history and currently applied filters are present
        # and properly formatted for the frontend to reference
        applied_filters = datalink_metadata["applied_filters"]
        assert isinstance(applied_filters[0], dict)

        sample_history = datalink_metadata["sample_history"]
        assert len(sample_history) == 1
        assert "filters" in sample_history[0]
        assert isinstance(sample_history[0]["filters"], list)
        assert isinstance(sample_history[0]["filters"][0], dict)
        assert sample_history[0]["filters"][0] == filters[0]
        assert sample_history[0]["sampling_time"] is not None

    assert datalink_metadata["sampling_time"] is not None

    assert datalink_metadata["dataframe_info"]["orig_num_rows"] == sample_dxdataframe.df.shape[0]
    assert datalink_metadata["dataframe_info"]["orig_num_cols"] == sample_dxdataframe.df.shape[1]


class TestResample:
    @pytest.mark.parametrize("has_filters", [True, False])
    @pytest.mark.parametrize("display_mode", ["simple", "enhanced"])
    def test_resample_from_db(
        self,
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
        self,
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
        self,
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
                sql_filter = (
                    f"SELECT * FROM {{table_name}} WHERE {sql_filter_str} LIMIT {sample_size}"
                )
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

    @pytest.mark.parametrize("has_filters", [True, False])
    @pytest.mark.parametrize("display_mode", ["simple", "enhanced"])
    def test_resample_associates_subset_to_parent(
        self,
        mocker,
        get_ipython: TerminalInteractiveShell,
        sample_random_dataframe: pd.DataFrame,
        sample_db_connection: duckdb.DuckDBPyConnection,
        sample_dex_filters: list,
        display_mode: str,
        has_filters: bool,
    ):
        """
        Ensure subsets resulting from dataframes are properly associated to
        their parent dataframe display ID and cell ID.
        """
        cell1 = str(uuid.uuid4())
        os.environ["LAST_EXECUTED_CELL_ID"] = cell1

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
                sql_filter = (
                    f"SELECT * FROM {{table_name}} WHERE {sql_filter_str} LIMIT {sample_size}"
                )
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
                    cell_id=cell1,
                )
            except Exception as e:
                assert False, f"Resample failed with error: {e}"

            resampled_dxdf = DXDataFrame(resampled_df)
            assert resampled_dxdf.cell_id == cell1
            assert resampled_dxdf.display_id == metadata[settings.MEDIA_TYPE]["display_id"]

            assert resampled_dxdf.hash in SUBSET_HASH_TO_PARENT_DATA
            assert (
                resampled_dxdf.cell_id == SUBSET_HASH_TO_PARENT_DATA[resampled_dxdf.hash]["cell_id"]
            )
            assert (
                resampled_dxdf.display_id
                == SUBSET_HASH_TO_PARENT_DATA[resampled_dxdf.hash]["display_id"]
            )

            if has_filters:
                applied_filter = resampled_dxdf.metadata["datalink"]["applied_filters"][0]
                assert isinstance(applied_filter, dict)

    @pytest.mark.parametrize("has_filters", [True, False])
    @pytest.mark.parametrize("display_mode", ["simple", "enhanced"])
    def test_resample_associates_subset_to_parent_after_other_execution(
        self,
        mocker,
        get_ipython: TerminalInteractiveShell,
        sample_random_dataframe: pd.DataFrame,
        sample_db_connection: duckdb.DuckDBPyConnection,
        sample_dex_filters: list,
        display_mode: str,
        has_filters: bool,
    ):
        """
        Ensure subsets resulting from dataframes are properly associated to
        their parent dataframe display ID and cell ID, even if LAST_EXECUTED_CELL_ID
        is different.

        This checks that DXDataFrames are properly pulling display_id/cell_id from
        SUBSET_HASH_TO_PARENT_DATA, and the cell_id is not relying primarily on
        the LAST_EXECUTED_CELL_ID environment variable.
        """
        cell1 = str(uuid.uuid4())
        os.environ["LAST_EXECUTED_CELL_ID"] = "some_other_cell"

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
                sql_filter = (
                    f"SELECT * FROM {{table_name}} WHERE {sql_filter_str} LIMIT {sample_size}"
                )
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
                    cell_id=cell1,
                )
            except Exception as e:
                assert False, f"Resample failed with error: {e}"

            resampled_dxdf = DXDataFrame(resampled_df)
            assert resampled_dxdf.cell_id == cell1
            assert resampled_dxdf.display_id == metadata[settings.MEDIA_TYPE]["display_id"]

            assert resampled_dxdf.hash in SUBSET_HASH_TO_PARENT_DATA
            assert (
                resampled_dxdf.cell_id == SUBSET_HASH_TO_PARENT_DATA[resampled_dxdf.hash]["cell_id"]
            )
            assert (
                resampled_dxdf.display_id
                == SUBSET_HASH_TO_PARENT_DATA[resampled_dxdf.hash]["display_id"]
            )
