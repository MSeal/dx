from dx.formatters.enhanced import get_dx_settings, register
from dx.formatters.main import DEFAULT_IPYTHON_DISPLAY_FORMATTER, DXDisplayFormatter
from dx.formatters.plain import get_pandas_settings, reset
from dx.formatters.simple import deregister, get_dataresource_settings
from dx.settings import get_settings, settings_context
from dx.shell import get_ipython_shell

dataresource_settings = get_dataresource_settings()
dx_settings = get_dx_settings()
pandas_settings = get_pandas_settings()
settings = get_settings()


def test_register_ipython_display_formatter():
    """
    Test that the display formatter for an IPython shell is
    successfully registered as a DXDisplayFormatter and that
    global settings have been properly updated.
    """
    with settings_context(display_mode="plain"):
        register()

        assert isinstance(get_ipython_shell().display_formatter, DXDisplayFormatter)

        settings_to_apply = {
            "DISPLAY_MAX_COLUMNS",
            "DISPLAY_MAX_ROWS",
            "MEDIA_TYPE",
            "FLATTEN_INDEX_VALUES",
            "FLATTEN_COLUMN_VALUES",
            "STRINGIFY_INDEX_VALUES",
            "STRINGIFY_COLUMN_VALUES",
        }
        for setting in settings_to_apply:
            val = getattr(dx_settings, f"DX_{setting}", None)
            assert getattr(settings, setting) == val


def test_deregister_ipython_display_formatter():
    """
    Test that the display formatter for an IPython shell is
    successfully registered as a DXDisplayFormatter
    and that global settings have been properly updated.
    """
    with settings_context(display_mode="plain"):
        deregister()

        assert isinstance(get_ipython_shell().display_formatter, DXDisplayFormatter)

        settings_to_apply = {
            "DISPLAY_MAX_COLUMNS",
            "DISPLAY_MAX_ROWS",
            "MEDIA_TYPE",
            "FLATTEN_INDEX_VALUES",
            "FLATTEN_COLUMN_VALUES",
            "STRINGIFY_INDEX_VALUES",
            "STRINGIFY_COLUMN_VALUES",
        }
        for setting in settings_to_apply:
            val = getattr(dataresource_settings, f"DATARESOURCE_{setting}", None)
            assert getattr(settings, setting) == val


def test_reset_ipython_display_formatter():
    """
    Test that the display formatter reverts to the default
    `IPython.core.formatters.DisplayFormatter` after resetting
    and that global settings have been properly updated.
    """
    with settings_context(display_mode="simple"):
        reset()

        assert get_ipython_shell().display_formatter == DEFAULT_IPYTHON_DISPLAY_FORMATTER
        assert not isinstance(get_ipython_shell().display_formatter, DXDisplayFormatter)


def test_default_media_types_remain():
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

    with settings_context(display_mode="plain"):
        deregister()
        dataresource_formatter_keys = set(get_ipython_shell().display_formatter.formatters.keys())
        assert dataresource_formatter_keys & default_media_types == default_media_types

    with settings_context(display_mode="plain"):
        register()
        dx_formatter_keys = set(get_ipython_shell().display_formatter.formatters.keys())
        assert dx_formatter_keys & default_media_types == default_media_types
