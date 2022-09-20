import numpy as np
import pandas as pd
import pytest
from IPython.terminal.interactiveshell import TerminalInteractiveShell

from dx.formatters.enhanced import get_dx_settings
from dx.formatters.main import DXDisplayFormatter, generate_body, handle_format
from dx.formatters.simple import get_dataresource_settings
from dx.settings import settings_context

dataresource_settings = get_dataresource_settings()
dx_settings = get_dx_settings()


class TestMediaTypes:
    def test_simple_media_type(
        self,
        sample_dataframe: pd.DataFrame,
        get_ipython: TerminalInteractiveShell,
    ):
        """
        Test "simple" display mode formatting returns the right media types
        and doesn't fail at any point with a basic dataframe.
        """
        with settings_context(display_mode="simple"):
            payload, metadata = handle_format(sample_dataframe, ipython_shell=get_ipython)
        assert dataresource_settings.DATARESOURCE_MEDIA_TYPE in payload
        assert dataresource_settings.DATARESOURCE_MEDIA_TYPE in metadata

    def test_enhanced_media_type(
        self,
        sample_dataframe: pd.DataFrame,
        get_ipython: TerminalInteractiveShell,
    ):
        """
        Test "enhanced" display mode formatting returns the right media types
        and doesn't fail at any point with a basic dataframe.
        """
        with settings_context(display_mode="enhanced"):
            payload, metadata = handle_format(sample_dataframe, ipython_shell=get_ipython)
        assert dx_settings.DX_MEDIA_TYPE in payload
        assert dx_settings.DX_MEDIA_TYPE in metadata


class TestDuplicateIndexValues:
    def test_simple_nonunique_index_succeeds(
        self,
        sample_dataframe: pd.DataFrame,
        get_ipython: TerminalInteractiveShell,
    ):
        """
        Test "simple" display mode formatting doesn't fail while formatting
        a dataframe with duplicate series and index values.
        """
        double_df = pd.concat([sample_dataframe, sample_dataframe])
        try:
            with settings_context(display_mode="simple"):
                handle_format(double_df, ipython_shell=get_ipython)
        except Exception as e:
            assert False, f"{e}"

    def test_enhanced_nonunique_index_succeeds(
        self,
        sample_dataframe: pd.DataFrame,
        get_ipython: TerminalInteractiveShell,
    ):
        """
        Test "enhanced" formatting doesn't fail while formatting
        a dataframe with duplicate series and index values.
        """
        double_df = pd.concat([sample_dataframe, sample_dataframe])
        try:
            with settings_context(display_mode="enhanced"):
                handle_format(double_df, ipython_shell=get_ipython)
        except Exception as e:
            assert False, f"{e}"


class TestMissingValues:
    @pytest.mark.parametrize("null_value", [None, np.nan, pd.NA])
    def test_simple_succeeds_with_missing_data(
        self,
        sample_dataframe: pd.DataFrame,
        get_ipython: TerminalInteractiveShell,
        null_value,
    ):
        """
        Test dataresource formatting doesn't fail while formatting
        a dataframe with null values.
        """
        sample_dataframe["missing_data"] = null_value
        try:
            with settings_context(display_mode="simple"):
                handle_format(sample_dataframe, ipython_shell=get_ipython)
        except Exception as e:
            assert False, f"{e}"

    @pytest.mark.parametrize("null_value", [None, np.nan, pd.NA])
    def test_enhanced_succeeds_with_missing_data(
        self,
        sample_dataframe: pd.DataFrame,
        get_ipython: TerminalInteractiveShell,
        null_value,
    ):
        """
        Test dx formatting doesn't fail while formatting
        a dataframe with null values.
        """
        sample_dataframe["missing_data"] = null_value
        try:
            with settings_context(display_mode="enhanced"):
                handle_format(sample_dataframe, ipython_shell=get_ipython)
        except Exception as e:
            assert False, f"{e}"

    @pytest.mark.parametrize("null_value", [np.nan, pd.NA])
    def test_simple_converts_na_to_none(self, null_value):
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
        with settings_context(display_mode="simple"):
            payload = generate_body(df)
        assert payload["data"][0] == {"index": 0, "foo": 1, "bar": "a"}
        assert payload["data"][1] == {"index": 1, "foo": 2, "bar": None}
        assert payload["data"][2] == {"index": 2, "foo": None, "bar": "b"}

    @pytest.mark.parametrize("null_value", [np.nan, pd.NA])
    def test_enhanced_converts_na_to_none(self, null_value):
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
        with settings_context(display_mode="enhanced"):
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
