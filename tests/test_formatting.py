import numpy as np
import pandas as pd
import pytest
from IPython.terminal.interactiveshell import TerminalInteractiveShell

from dx.formatters.enhanced import get_dx_settings
from dx.formatters.main import handle_format
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
