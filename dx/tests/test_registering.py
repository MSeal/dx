import pandas as pd
from dx.formatters.dataresource import (
    DXDataResourceDisplayFormatter,
    deregister,
    get_dataresource_settings,
)
from dx.formatters.dx import DXDisplayFormatter, get_dx_settings, register
from dx.formatters.main import get_pandas_settings, reset
from dx.settings import get_settings
from IPython.terminal.interactiveshell import TerminalInteractiveShell

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
    register(ipython_shell=get_ipython)
    assert isinstance(get_ipython.display_formatter, DXDisplayFormatter)

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
    register(ipython_shell=get_ipython)
    assert isinstance(get_ipython.display_formatter, DXDisplayFormatter)

    deregister(ipython_shell=get_ipython)
    assert isinstance(get_ipython.display_formatter, DXDataResourceDisplayFormatter)

    assert (
        settings.DISPLAY_MAX_COLUMNS
        == dataresource_settings.DATARESOURCE_DISPLAY_MAX_COLUMNS
    )
    assert (
        settings.DISPLAY_MAX_ROWS == dataresource_settings.DATARESOURCE_DISPLAY_MAX_ROWS
    )

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
    deregister(ipython_shell=get_ipython)
    assert isinstance(get_ipython.display_formatter, DXDataResourceDisplayFormatter)

    reset(ipython_shell=get_ipython)
    # TODO: write new test that checks for basic `IPython.core.formatters.DisplayFormatter`?
    assert get_ipython.display_formatter is None

    assert settings.DISPLAY_MAX_COLUMNS == pandas_settings.PANDAS_DISPLAY_MAX_COLUMNS
    assert settings.DISPLAY_MAX_ROWS == pandas_settings.PANDAS_DISPLAY_MAX_ROWS

    assert pd.get_option("display.max_columns") == settings.DISPLAY_MAX_COLUMNS
    assert pd.get_option("display.max_rows") == settings.DISPLAY_MAX_ROWS
