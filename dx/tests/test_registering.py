import pandas as pd
from dx.formatters.dataresource import (
    DATARESOURCE_DISPLAY_MAX_ROWS,
    DATARESOURCE_HTML_TABLE_SCHEMA,
    DXDataResourceDisplayFormatter,
    deregister,
)
from dx.formatters.dx import (
    DX_DISPLAY_MAX_ROWS,
    DX_HTML_TABLE_SCHEMA,
    DXDisplayFormatter,
    register,
)
from dx.formatters.main import (
    DEFAULT_DISPLAY_MAX_ROWS,
    DEFAULT_HTML_TABLE_SCHEMA,
    reset,
)
from IPython.terminal.interactiveshell import TerminalInteractiveShell


def test_register_ipython_display_formatter(
    get_ipython: TerminalInteractiveShell,
):  # noqa: E501
    """
    Test that the display formatter for an IPython shell is
    successfully registered as a DXDisplayFormatter.
    """
    register(ipython_shell=get_ipython)
    assert isinstance(get_ipython.display_formatter, DXDisplayFormatter)

    assert pd.get_option("html.table_schema") == DX_HTML_TABLE_SCHEMA
    assert pd.get_option("display.max_rows") == DX_DISPLAY_MAX_ROWS


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

    assert pd.get_option("html.table_schema") == DATARESOURCE_HTML_TABLE_SCHEMA
    assert pd.get_option("display.max_rows") == DATARESOURCE_DISPLAY_MAX_ROWS


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

    assert pd.get_option("html.table_schema") == DEFAULT_HTML_TABLE_SCHEMA
    assert pd.get_option("display.max_rows") == DEFAULT_DISPLAY_MAX_ROWS
