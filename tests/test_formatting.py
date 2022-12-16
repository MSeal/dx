import numpy as np
import pandas as pd
import pytest
from IPython.terminal.interactiveshell import TerminalInteractiveShell

from dx.formatters.enhanced import get_dx_settings
from dx.formatters.main import DXDisplayFormatter, generate_body, handle_format
from dx.formatters.simple import get_dataresource_settings
from dx.settings import get_settings, settings_context
from dx.utils.formatting import (
    check_for_duplicate_columns,
    groupby_series_index_name,
    incrementing_label,
    normalize_index_and_columns,
    to_dataframe,
)
from dx.utils.tracking import DXDF_CACHE

dataresource_settings = get_dataresource_settings()
dx_settings = get_dx_settings()
settings = get_settings()


class TestMediaTypes:
    @pytest.mark.parametrize("datalink_enabled", [True, False])
    def test_simple_media_type(
        self,
        sample_dataframe: pd.DataFrame,
        get_ipython: TerminalInteractiveShell,
        datalink_enabled: bool,
    ):
        """
        Test "simple" display mode formatting returns the right media types
        and doesn't fail at any point with a basic dataframe.
        """
        with settings_context(enable_datalink=datalink_enabled, display_mode="simple"):
            payload, metadata = handle_format(sample_dataframe, ipython_shell=get_ipython)
        assert dataresource_settings.DATARESOURCE_MEDIA_TYPE in payload
        assert dataresource_settings.DATARESOURCE_MEDIA_TYPE in metadata

    @pytest.mark.parametrize("datalink_enabled", [True, False])
    def test_enhanced_media_type(
        self,
        sample_dataframe: pd.DataFrame,
        get_ipython: TerminalInteractiveShell,
        datalink_enabled: bool,
    ):
        """
        Test "enhanced" display mode formatting returns the right media types
        and doesn't fail at any point with a basic dataframe.
        """
        with settings_context(enable_datalink=datalink_enabled, display_mode="enhanced"):
            payload, metadata = handle_format(sample_dataframe, ipython_shell=get_ipython)
        assert dx_settings.DX_MEDIA_TYPE in payload
        assert dx_settings.DX_MEDIA_TYPE in metadata


class TestDuplicateIndexValues:
    @pytest.mark.parametrize("display_mode", ["simple", "enhanced"])
    @pytest.mark.parametrize("datalink_enabled", [True, False])
    def test_nonunique_index_succeeds(
        self,
        sample_dataframe: pd.DataFrame,
        get_ipython: TerminalInteractiveShell,
        datalink_enabled: bool,
        display_mode: str,
    ):
        """
        Test simple/enhanced display modes succeed while formatting
        a dataframe with duplicate series and index values, and
        the resulting payload represents a dataframe after a .reset_index()
        so the index values going to the frontend have unique values.
        """
        double_df = pd.concat([sample_dataframe, sample_dataframe])
        try:
            with settings_context(
                enable_datalink=datalink_enabled,
                display_mode=display_mode,
            ):
                handle_format(double_df, ipython_shell=get_ipython)
        except Exception as e:
            assert False, f"{e}"


class TestMissingValues:
    @pytest.mark.parametrize("null_value", [None, np.nan, pd.NA])
    @pytest.mark.parametrize("datalink_enabled", [True, False])
    def test_simple_succeeds_with_missing_data(
        self,
        sample_dataframe: pd.DataFrame,
        get_ipython: TerminalInteractiveShell,
        null_value,
        datalink_enabled: bool,
    ):
        """
        Test dataresource formatting doesn't fail while formatting
        a dataframe with null values.
        """
        sample_dataframe["missing_data"] = null_value
        try:
            with settings_context(enable_datalink=datalink_enabled, display_mode="simple"):
                handle_format(sample_dataframe, ipython_shell=get_ipython)
        except Exception as e:
            assert False, f"{e}"

    @pytest.mark.parametrize("null_value", [None, np.nan, pd.NA])
    @pytest.mark.parametrize("datalink_enabled", [True, False])
    def test_enhanced_succeeds_with_missing_data(
        self,
        sample_dataframe: pd.DataFrame,
        get_ipython: TerminalInteractiveShell,
        null_value,
        datalink_enabled: bool,
    ):
        """
        Test dx formatting doesn't fail while formatting
        a dataframe with null values.
        """
        sample_dataframe["missing_data"] = null_value
        try:
            with settings_context(enable_datalink=datalink_enabled, display_mode="enhanced"):
                handle_format(sample_dataframe, ipython_shell=get_ipython)
        except Exception as e:
            assert False, f"{e}"

    @pytest.mark.parametrize("null_value", [np.nan, pd.NA])
    @pytest.mark.parametrize("datalink_enabled", [True, False])
    def test_simple_converts_na_to_none(
        self,
        null_value,
        datalink_enabled: bool,
    ):
        """
        Test "simple" display mode properly converts `pd.NA` and `NaN`
        values to `None` before passing along the payload.
        """
        df = pd.DataFrame(
            {
                "foo": [1, 2, null_value],
                "bar": ["a", null_value, "b"],
            }
        )
        with settings_context(enable_datalink=datalink_enabled, display_mode="simple"):
            payload = generate_body(df)
        assert payload["data"][0] == {"index": 0, "foo": 1, "bar": "a"}
        assert payload["data"][1] == {"index": 1, "foo": 2, "bar": None}
        assert payload["data"][2] == {"index": 2, "foo": None, "bar": "b"}

    @pytest.mark.parametrize("null_value", [np.nan, pd.NA])
    @pytest.mark.parametrize("datalink_enabled", [True, False])
    @pytest.mark.parametrize("display_mode", ["simple", "enhanced"])
    def test_enhanced_converts_na_to_none(
        self,
        null_value,
        datalink_enabled: bool,
        display_mode: str,
    ):
        """
        Test dx formatting properly converts `pd.NA` and `NaN`
        values to `None` before passing along the payload.
        """
        df = pd.DataFrame(
            {
                "foo": [1, 2, null_value],
                "bar": ["a", null_value, "b"],
            }
        )
        with settings_context(enable_datalink=datalink_enabled, display_mode="enhanced"):
            payload = generate_body(df)
        assert payload["data"][1] == [1, 2, None]
        assert payload["data"][2] == ["a", None, "b"]


class TestDisplayFormatter:
    def test_text(self):
        """
        Test the text formatter returns the right media type.
        """
        value = "hello, world!"
        formatter = DXDisplayFormatter()
        formatted_value = formatter.format(value)
        assert formatted_value == ({"text/plain": "'hello, world!'"}, {})

    def test_dataframe(self, sample_dataframe: pd.DataFrame, mocker):
        """
        Test that dataframes are captured by the formatter
        and do not return a tuple of payload/metadata dictionaries.

        (This is because the formatter registers a display ID to be used
        by `IPython.display`.)
        """
        formatter = DXDisplayFormatter()
        mocker.patch("dx.formatters.main.IN_NOTEBOOK_ENV", True)
        formatted_value = formatter.format(sample_dataframe)
        assert formatted_value == ({}, {})


class TestDataFrameHandling:
    @pytest.mark.parametrize("display_mode", ["simple", "enhanced"])
    @pytest.mark.parametrize("datalink_enabled", [True, False])
    @pytest.mark.parametrize(
        "data_structure",
        [
            "sample_dataframe",
            "sample_groupby_series",
            "sample_groupby_dataframe",
            "sample_resampled_dataframe",
            "sample_resampled_groupby_dataframe",
            "sample_random_dataframe_with_duplicate_columns",
        ],
    )
    def test_success_with_varying_dataframe_structures(
        self,
        data_structure,
        get_ipython: TerminalInteractiveShell,
        datalink_enabled: bool,
        display_mode: str,
        sample_dataframe: pd.DataFrame,
        sample_groupby_series: pd.Series,
        sample_groupby_dataframe: pd.DataFrame,
        sample_resampled_dataframe: pd.DataFrame,
        sample_resampled_groupby_dataframe: pd.DataFrame,
        sample_random_dataframe_with_duplicate_columns: pd.DataFrame,
    ):
        """
        Test that various operations applied to dataframes will still
        be formatted without error across the different display modes
        and with datalink enabled/disabled.
        """
        if data_structure == "sample_dataframe":
            obj = sample_dataframe
        elif data_structure == "sample_groupby_series":
            obj = sample_groupby_series
        elif data_structure == "sample_groupby_dataframe":
            obj = sample_groupby_dataframe
        elif data_structure == "sample_resampled_dataframe":
            obj = sample_resampled_dataframe
        elif data_structure == "sample_resampled_groupby_dataframe":
            obj = sample_resampled_groupby_dataframe
        elif data_structure == "sample_random_dataframe_with_duplicate_columns":
            obj = sample_random_dataframe_with_duplicate_columns

        try:
            with settings_context(enable_datalink=datalink_enabled, display_mode=display_mode):
                handle_format(obj, ipython_shell=get_ipython)
        except Exception as e:
            assert False, f"{e}"


class TestRenderableTypes:
    @pytest.mark.parametrize("renderable_type", [np.ndarray, pd.Series])
    @pytest.mark.parametrize("datalink_enabled", [True, False])
    def test_simple_succeeds_with_default_renderable_types(
        self,
        renderable_type,
        datalink_enabled: bool,
        sample_random_dataframe: pd.DataFrame,
        get_ipython: TerminalInteractiveShell,
    ):
        """
        Test "simple" display mode formatting doesn't fail while
        formatting a supported renderable data type that isn't a pandas DataFrame,
        to include the additional processing and tracking handled for datalink.

        Additionally, if datalink is enabled, ensure that the display ID was
        generated within the DXDataFrame and stored in the DXDF_CACHE.
        """
        if renderable_type is np.ndarray:
            data = sample_random_dataframe.values
        elif renderable_type is pd.Series:
            data = sample_random_dataframe["keyword_column"]

        try:
            with settings_context(enable_datalink=datalink_enabled, display_mode="simple"):
                _, metadata = handle_format(data, ipython_shell=get_ipython)
                if datalink_enabled:
                    display_id = metadata[settings.MEDIA_TYPE]["display_id"]
                    assert display_id in DXDF_CACHE
        except Exception as e:
            assert False, f"{e}"

    @pytest.mark.parametrize("renderable_type", [np.ndarray, pd.Series])
    @pytest.mark.parametrize("datalink_enabled", [True, False])
    def test_enhanced_succeeds_with_default_renderable_types(
        self,
        renderable_type,
        datalink_enabled: bool,
        sample_random_dataframe: pd.DataFrame,
        get_ipython: TerminalInteractiveShell,
    ):
        """
        Test "enhanced" display mode formatting doesn't fail while
        formatting a supported renderable data type that isn't a pandas DataFrame,
        to include the additional processing and tracking handled for datalink.

        Additionally, if datalink is enabled, ensure that the display ID was
        generated within the DXDataFrame and stored in the DXDF_CACHE.
        """
        if renderable_type is np.ndarray:
            data = sample_random_dataframe.values
        elif renderable_type is pd.Series:
            data = sample_random_dataframe["keyword_column"]

        try:
            with settings_context(enable_datalink=datalink_enabled, display_mode="enhanced"):
                _, metadata = handle_format(data, ipython_shell=get_ipython)
                if datalink_enabled:
                    display_id = metadata[settings.MEDIA_TYPE]["display_id"]
                    assert display_id in DXDF_CACHE
        except Exception as e:
            assert False, f"{e}"


class TestIndexColumnNormalizing:
    def test_sample_dataframe(self, sample_dataframe: pd.DataFrame):
        """
        Test that a basic dataframe will keep its original index
        and column structure after being passed through normalize_index_and_columns().
        """
        clean_df = normalize_index_and_columns(sample_dataframe)
        assert clean_df.index.equals(sample_dataframe.index)
        assert clean_df.columns.equals(sample_dataframe.columns)

    def test_sample_resampled_groupby_dataframe(self, sample_random_dataframe: pd.DataFrame):
        """
        Test that a resampled groupby dataframe will keep its original index,
        but if the dataframe has a MultiIndex with a name that conflicts with
        one of the dataframe columns, the duplicate column will have `.value`
        appended so .reset_index() doesn't break.
        """
        # same as the `sample_resampled_groupby_dataframe` fixture,
        # but defining the columns here makes for easier readability
        sample_resampled_groupby_dataframe = (
            sample_random_dataframe.groupby("keyword_column")
            .resample("1D", on="datetime_column")
            .min()
        )
        # this will add `keyword_column` and `datetime_column` as levels in the .index, but `keyword_column` will remain in the .columns
        clean_df = normalize_index_and_columns(sample_resampled_groupby_dataframe)
        assert clean_df.index.equals(sample_resampled_groupby_dataframe.index)
        assert "keyword_column" not in clean_df.columns
        assert "keyword_column.value" in clean_df.columns

    def test_sample_resampled_multi_groupby_dataframe(self, sample_random_dataframe: pd.DataFrame):
        """
        Test that a resampled groupby dataframe will keep its original index,
        but if the dataframe has a MultiIndex with names that conflict with
        the dataframe columns, the duplicate columns will have `.value` appended
        so .reset_index() doesn't break.
        """
        # same as the `sample_resampled_groupby_dataframe` fixture,
        # but defining the columns here makes for easier readability
        sample_resampled_groupby_dataframe = (
            sample_random_dataframe.groupby(["keyword_column", "integer_column"])
            .resample("1D", on="datetime_column")
            .min()
        )
        # this will add `keyword_column`, `integer_column`, and `datetime_column`
        # as levels in the .index, but `keyword_column` and `integer_column`
        # will remain in the .columns
        clean_df = normalize_index_and_columns(sample_resampled_groupby_dataframe)
        assert clean_df.index.equals(sample_resampled_groupby_dataframe.index)
        assert "keyword_column" not in clean_df.columns
        assert "keyword_column.value" in clean_df.columns
        assert "integer_column" not in clean_df.columns
        assert "integer_column.value" in clean_df.columns


class TestDataFrameConversion:
    def test_series_is_converted(self, sample_random_dataframe: pd.Series):
        """
        Test that a basic conversion from pd.Series to pd.Dataframe
        keeps the original index and uses the Series name as its only column.
        """
        s: pd.Series = sample_random_dataframe.keyword_column
        df = to_dataframe(s)
        assert df.index.equals(s.index)
        assert df.columns[0] == s.name

    def test_multiindex_series_left_alone(self, sample_multiindex_series: pd.Series):
        """
        Test no renaming is done with a MultiIndex pd.Series if their
        name doesn't appear in the MultiIndex names.
        """
        index = sample_multiindex_series.index
        df = to_dataframe(sample_multiindex_series)
        assert df.index.names == index.names
        assert df.columns[0] == sample_multiindex_series.name

    def test_groupby_series_resets(self, sample_groupby_series: pd.Series):
        """
        Test we're resetting the index of a pd.Series created from a groupby
        operation by using the combination of index names.
        """
        index = sample_groupby_series.index
        df = to_dataframe(sample_groupby_series)
        assert df.index.names == index.names
        assert df.columns[0] == groupby_series_index_name(index)
        assert df.columns[0] != sample_groupby_series.name

    def test_dataframe_index_left_alone(self, sample_random_dataframe: pd.DataFrame):
        """
        Ensure we don't alter the structure of a dataframe during
        initial dataframe conversion.
        """
        df = to_dataframe(sample_random_dataframe)
        assert df.index.equals(sample_random_dataframe.index)
        assert df.columns.equals(sample_random_dataframe.columns)

    def test_groupby_dataframe_index_left_alone(self, sample_groupby_dataframe: pd.DataFrame):
        """
        Ensure we don't alter the structure of a dataframe
        with MultiIndexes during initial dataframe conversion.
        """
        df = to_dataframe(sample_groupby_dataframe)
        assert df.index.equals(sample_groupby_dataframe.index)
        assert df.columns.equals(sample_groupby_dataframe.columns)


class TestMetadataStructure:
    @pytest.mark.parametrize("display_mode", ["simple", "enhanced"])
    def test_variable_name_exists(
        self,
        sample_random_dataframe: pd.DataFrame,
        get_ipython: TerminalInteractiveShell,
        display_mode: str,
    ):
        """
        Ensure that the variable name is present in the metadata.
        """
        with settings_context(
            enable_datalink=True,
            display_mode=display_mode,
        ):
            _, metadata = handle_format(sample_random_dataframe, ipython_shell=get_ipython)
            display_metadata = metadata[settings.MEDIA_TYPE]

        assert "datalink" in display_metadata
        assert "display_id" in display_metadata

        datalink_metadata = display_metadata["datalink"]
        assert "variable_name" in datalink_metadata
        assert "dataframe_info" in datalink_metadata

        assert (
            datalink_metadata["dataframe_info"]["orig_num_rows"] == sample_random_dataframe.shape[0]
        )
        assert (
            datalink_metadata["dataframe_info"]["orig_num_cols"] == sample_random_dataframe.shape[1]
        )

        assert "dx_settings" in datalink_metadata
        assert isinstance(datalink_metadata["applied_filters"], list)
        assert isinstance(datalink_metadata["sample_history"], list)


class TestMetadataVariableName:
    @pytest.mark.parametrize("display_mode", ["simple", "enhanced"])
    def test_assigned_variable_name_matches(
        self,
        sample_random_dataframe: pd.DataFrame,
        get_ipython: TerminalInteractiveShell,
        display_mode: str,
    ):
        """
        Ensure that the assigned variable name is present in the metadata.
        """
        get_ipython.user_ns["test_df"] = sample_random_dataframe

        with settings_context(
            enable_datalink=True,
            display_mode=display_mode,
        ):
            _, metadata = handle_format(sample_random_dataframe, ipython_shell=get_ipython)
            display_metadata = metadata[settings.MEDIA_TYPE]
            assert display_metadata["datalink"]["variable_name"] == "test_df"

    @pytest.mark.parametrize("display_mode", ["simple", "enhanced"])
    def test_unassigned_variable_name_present(
        self,
        sample_random_dataframe: pd.DataFrame,
        get_ipython: TerminalInteractiveShell,
        display_mode: str,
    ):
        """
        Ensure that our placeholder variable name is present in the metadata.
        """
        with settings_context(
            enable_datalink=True,
            display_mode=display_mode,
        ):
            _, metadata = handle_format(sample_random_dataframe, ipython_shell=get_ipython)
            display_metadata = metadata[settings.MEDIA_TYPE]
            assert display_metadata["datalink"]["variable_name"].startswith("unk_dataframe")

    @pytest.mark.parametrize("display_mode", ["simple", "enhanced"])
    def test_empty_variable_name_with_datalink_disabled(
        self,
        sample_random_dataframe: pd.DataFrame,
        get_ipython: TerminalInteractiveShell,
        display_mode: str,
    ):
        """
        Ensure that our placeholder variable name is present in the metadata.

        (With datalink disabled, no cleaning/hashing/variable association will be done.)
        """
        with settings_context(
            enable_datalink=False,
            display_mode=display_mode,
        ):
            _, metadata = handle_format(sample_random_dataframe, ipython_shell=get_ipython)
            display_metadata = metadata[settings.MEDIA_TYPE]
            assert display_metadata["datalink"]["variable_name"] == ""


class TestDuplicateColumns:
    def test_duplicate_columns_add_suffixes(
        self, sample_random_dataframe_with_duplicate_columns: pd.DataFrame
    ):
        """
        Ensure that duplicate columns are handled correctly.
        """
        df = check_for_duplicate_columns(sample_random_dataframe_with_duplicate_columns)
        assert not df.columns.duplicated().any()

    def test_duplicate_columns_add_suffixes_with_groupby(
        self, sample_random_dataframe_with_duplicate_columns: pd.DataFrame
    ):
        """
        Ensure that duplicate columns are handled correctly when grouping.
        """
        duped_groupby = sample_random_dataframe_with_duplicate_columns.groupby(
            "keyword_column"
        ).agg(["min", "max"])
        df = check_for_duplicate_columns(duped_groupby)
        assert not df.columns.duplicated().any()


class TestIncrementingLabels:
    def test_single_label(self):
        """
        Ensure that a string present in an iterable is appended with
        a numeric suffix.
        """
        test_value = "a"
        values = ["a", "b", "c"]
        test_value = incrementing_label(test_value, values)
        assert test_value == "a_1"

    def test_multiple_labels(self):
        """
        Ensure that a string present in an iterable multiple times
        is appended with the correct numeric suffix.
        """
        test_value = "a"
        values = ["a", "a_1", "a_2", "b", "c"]
        test_value = incrementing_label(test_value, values)
        assert test_value == "a_3"
