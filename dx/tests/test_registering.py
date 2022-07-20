import pandas as pd
from dx.formatters.dataresource import DXDataResourceDisplayFormatter, deregister
from dx.formatters.dx import DXDisplayFormatter, register
from dx.formatters.main import reset
from dx.settings import get_settings
from IPython.terminal.interactiveshell import TerminalInteractiveShell

settings = get_settings()


def test_register_ipython_display_formatter(
    get_ipython: TerminalInteractiveShell,
):  # noqa: E501
    """
    Test that the display formatter for an IPython shell is
    successfully registered as a DXDisplayFormatter.
    """
    register(ipython_shell=get_ipython)
    assert isinstance(get_ipython.display_formatter, DXDisplayFormatter)

    assert pd.get_option("html.table_schema") == settings.DX_HTML_TABLE_SCHEMA
    assert pd.get_option("display.max_rows") == settings.DX_DISPLAY_MAX_ROWS


def test_deregister_ipython_display_formatter(
    get_ipython: TerminalInteractiveShell,
):  # noqa: E501
    """
    Test that the display formatter for an IPython shell is
    successfully registered as a DXDataResourceDisplayFormatter.
    """
    register(ipython_shell=get_ipython)
    assert isinstance(get_ipython.display_formatter, DXDisplayFormatter)

    deregister(ipython_shell=get_ipython)
    assert isinstance(get_ipython.display_formatter, DXDataResourceDisplayFormatter)

    assert pd.get_option("html.table_schema") == settings.DATARESOURCE_HTML_TABLE_SCHEMA
    assert pd.get_option("display.max_rows") == settings.DATARESOURCE_DISPLAY_MAX_ROWS


def test_reset_ipython_display_formatter(
    get_ipython: TerminalInteractiveShell,
):  # noqa: E501
    """
    Test that the display formatter reverts to the default
    `IPython.core.formatters.DisplayFormatter` after resetting.
    """
    deregister(ipython_shell=get_ipython)
    assert isinstance(get_ipython.display_formatter, DXDataResourceDisplayFormatter)

    reset(ipython_shell=get_ipython)
    # TODO: write new test that checks for basic `IPython.core.formatters.DisplayFormatter`?
    assert get_ipython.display_formatter is None

    assert pd.get_option("html.table_schema") == settings.PANDAS_HTML_TABLE_SCHEMA
    assert pd.get_option("display.max_rows") == settings.PANDAS_DISPLAY_MAX_ROWS
