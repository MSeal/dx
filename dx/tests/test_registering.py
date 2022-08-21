import pandas as pd
from IPython.terminal.interactiveshell import TerminalInteractiveShell

from dx.formatters.dataresource import deregister, get_dataresource_settings
from dx.formatters.dx import get_dx_settings, register
from dx.formatters.main import get_pandas_settings, reset
from dx.settings import get_settings

dataresource_settings = get_dataresource_settings()
dx_settings = get_dx_settings()
pandas_settings = get_pandas_settings()
settings = get_settings()


def test_register_ipython_display_formatter(
    get_ipython: TerminalInteractiveShell,
):  # noqa: E501
    """
    Test that the display formatter for an IPython shell is
    successfully registered as a DXDisplayFormatter and that
    global settings have been properly updated.
    """
    formatters = get_ipython.display_formatter.formatters

    register(ipython_shell=get_ipython)
    assert dataresource_settings.DATARESOURCE_MEDIA_TYPE not in formatters
    assert dx_settings.DX_MEDIA_TYPE in formatters

    assert settings.DISPLAY_MAX_COLUMNS == dx_settings.DX_DISPLAY_MAX_COLUMNS
    assert settings.DISPLAY_MAX_ROWS == dx_settings.DX_DISPLAY_MAX_ROWS

    assert pd.get_option("display.max_columns") == settings.DISPLAY_MAX_COLUMNS
    assert pd.get_option("display.max_rows") == settings.DISPLAY_MAX_ROWS


def test_deregister_ipython_display_formatter(
    get_ipython: TerminalInteractiveShell,
):  # noqa: E501
    """
    Test that the display formatter for an IPython shell is
    successfully registered as a DXDataResourceDisplayFormatter
    and that global settings have been properly updated.
    """
    formatters = get_ipython.display_formatter.formatters

    register(ipython_shell=get_ipython)
    assert dataresource_settings.DATARESOURCE_MEDIA_TYPE not in formatters
    assert dx_settings.DX_MEDIA_TYPE in formatters

    deregister(ipython_shell=get_ipython)
    assert dataresource_settings.DATARESOURCE_MEDIA_TYPE in formatters
    assert dx_settings.DX_MEDIA_TYPE not in formatters

    assert settings.DISPLAY_MAX_COLUMNS == dataresource_settings.DATARESOURCE_DISPLAY_MAX_COLUMNS
    assert settings.DISPLAY_MAX_ROWS == dataresource_settings.DATARESOURCE_DISPLAY_MAX_ROWS

    assert pd.get_option("display.max_columns") == settings.DISPLAY_MAX_COLUMNS
    assert pd.get_option("display.max_rows") == settings.DISPLAY_MAX_ROWS


def test_reset_ipython_display_formatter(
    get_ipython: TerminalInteractiveShell,
):  # noqa: E501
    """
    Test that the display formatter reverts to the default
    `IPython.core.formatters.DisplayFormatter` after resetting
    and that global settings have been properly updated.
    """
    formatters = get_ipython.display_formatter.formatters
    deregister(ipython_shell=get_ipython)
    assert dataresource_settings.DATARESOURCE_MEDIA_TYPE in formatters

    reset(ipython_shell=get_ipython)
    assert dataresource_settings.DATARESOURCE_MEDIA_TYPE not in formatters
    assert dx_settings.DX_MEDIA_TYPE not in formatters

    assert settings.DISPLAY_MAX_COLUMNS == pandas_settings.PANDAS_DISPLAY_MAX_COLUMNS
    assert settings.DISPLAY_MAX_ROWS == pandas_settings.PANDAS_DISPLAY_MAX_ROWS

    assert pd.get_option("display.max_columns") == settings.DISPLAY_MAX_COLUMNS
    assert pd.get_option("display.max_rows") == settings.DISPLAY_MAX_ROWS
