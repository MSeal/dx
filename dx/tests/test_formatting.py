import numpy as np
import pandas as pd
import pytest
from IPython.terminal.interactiveshell import TerminalInteractiveShell

from dx.formatters.dataresource import get_dataresource_settings, handle_dataresource_format
from dx.formatters.dx import get_dx_settings, handle_dx_format

dataresource_settings = get_dataresource_settings()
dx_settings = get_dx_settings()


def test_dataresource_media_type(
    sample_dataframe: pd.DataFrame,
    get_ipython: TerminalInteractiveShell,
):
    """
    Test dataresource formatting returns the right media types
    and doesn't fail at any point with a basic dataframe.
    """
    payload, metadata = handle_dataresource_format(sample_dataframe, ipython_shell=get_ipython)
    assert dataresource_settings.DATARESOURCE_MEDIA_TYPE in payload
    assert dataresource_settings.DATARESOURCE_MEDIA_TYPE in metadata


def test_dx_media_type(
    sample_dataframe: pd.DataFrame,
    get_ipython: TerminalInteractiveShell,
):
    """
    Test dx formatting returns the right media types
    and doesn't fail at any point with a basic dataframe.
    """
    payload, metadata = handle_dx_format(sample_dataframe, ipython_shell=get_ipython)
    assert dx_settings.DX_MEDIA_TYPE in payload
    assert dx_settings.DX_MEDIA_TYPE in metadata


def test_dataresource_nonunique_index_succeeds(
    sample_dataframe: pd.DataFrame,
    get_ipython: TerminalInteractiveShell,
):
    """
    Test dataresource formatting doesn't fail while formatting
    a dataframe with duplicate series and index values.
    """
    double_df = pd.concat([sample_dataframe, sample_dataframe])
    try:
        handle_dataresource_format(double_df, ipython_shell=get_ipython)
    except Exception as e:
        assert False, f"{e}"


def test_dx_nonunique_index_succeeds(
    sample_dataframe: pd.DataFrame,
    get_ipython: TerminalInteractiveShell,
):
    """
    Test dataresource formatting doesn't fail while formatting
    a dataframe with duplicate series and index values.
    """
    double_df = pd.concat([sample_dataframe, sample_dataframe])
    try:
        handle_dx_format(double_df, ipython_shell=get_ipython)
    except Exception as e:
        assert False, f"{e}"


@pytest.mark.parametrize("null_value", [None, np.nan, pd.NA])
def test_dataresource_succeeds_with_missing_data(
    sample_dataframe: pd.DataFrame,
    get_ipython: TerminalInteractiveShell,
    null_value,
):
    """
    Test dataresource formatting doesn't fail while formatting
    a dataframe with duplicate series and index values.
    """
    sample_dataframe["missing_data"] = null_value
    try:
        handle_dataresource_format(sample_dataframe, ipython_shell=get_ipython)
    except Exception as e:
        assert False, f"{e}"


@pytest.mark.parametrize("null_value", [None, np.nan, pd.NA])
def test_dx_succeeds_with_missing_data(
    sample_dataframe: pd.DataFrame,
    get_ipython: TerminalInteractiveShell,
    null_value,
):
    """
    Test dx formatting doesn't fail while formatting
    a dataframe with duplicate series and index values.
    """
    sample_dataframe["missing_data"] = null_value
    try:
        handle_dx_format(sample_dataframe, ipython_shell=get_ipython)
    except Exception as e:
        assert False, f"{e}"
