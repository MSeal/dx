from IPython.terminal.interactiveshell import TerminalInteractiveShell

from dx.formatters.dataresource import (
    DXDataResourceDisplayFormatter,
    deregister,
    get_dataresource_settings,
)
from dx.formatters.dx import DXDisplayFormatter, get_dx_settings, register
from dx.formatters.main import DEFAULT_IPYTHON_DISPLAY_FORMATTER, get_pandas_settings, reset
from dx.settings import get_settings, settings_context

dataresource_settings = get_dataresource_settings()
dx_settings = get_dx_settings()
pandas_settings = get_pandas_settings()
settings = get_settings()


def test_register_ipython_display_formatter(get_ipython: TerminalInteractiveShell):
    """
    Test that the display formatter for an IPython shell is
    successfully registered as a DXDisplayFormatter and that
    global settings have been properly updated.
    """
    with settings_context(ipython_shell=get_ipython, display_mode="plain"):
        register(ipython_shell=get_ipython)

        assert isinstance(get_ipython.display_formatter, DXDisplayFormatter)


def test_deregister_ipython_display_formatter(get_ipython: TerminalInteractiveShell):
    """
    Test that the display formatter for an IPython shell is
    successfully registered as a DXDataResourceDisplayFormatter
    and that global settings have been properly updated.
    """
    with settings_context(ipython_shell=get_ipython, display_mode="plain"):
        deregister(ipython_shell=get_ipython)

        assert isinstance(get_ipython.display_formatter, DXDataResourceDisplayFormatter)


def test_reset_ipython_display_formatter(get_ipython: TerminalInteractiveShell):
    """
    Test that the display formatter reverts to the default
    `IPython.core.formatters.DisplayFormatter` after resetting
    and that global settings have been properly updated.
    """
    with settings_context(ipython_shell=get_ipython, display_mode="simple"):
        reset(ipython_shell=get_ipython)

        assert get_ipython.display_formatter == DEFAULT_IPYTHON_DISPLAY_FORMATTER
        assert not isinstance(
            get_ipython.display_formatter, (DXDataResourceDisplayFormatter, DXDisplayFormatter)
        )


def test_default_media_types_remain(get_ipython: TerminalInteractiveShell):
    """
    Test that setting the dispay mode to "simple" or "enhanced" does not remove
    any existing formatters for unrelated media types:
        application/javascript
        application/json
        application/pdf
        text/html
        text/latex
        text/markdown
        text/plain
        image/jpeg
        image/png
        image/svg+xml
    """

    default_media_types = set(DEFAULT_IPYTHON_DISPLAY_FORMATTER.formatters.keys())
    assert default_media_types != set()

    with settings_context(ipython_shell=get_ipython, display_mode="plain"):
        deregister(ipython_shell=get_ipython)
        dataresource_formatter_keys = set(get_ipython.display_formatter.formatters.keys())
        assert dataresource_formatter_keys & default_media_types == default_media_types

    with settings_context(ipython_shell=get_ipython, display_mode="plain"):
        register(ipython_shell=get_ipython)
        dx_formatter_keys = set(get_ipython.display_formatter.formatters.keys())
        assert dx_formatter_keys & default_media_types == default_media_types
