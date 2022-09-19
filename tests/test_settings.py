from IPython.terminal.interactiveshell import TerminalInteractiveShell

from dx.settings import add_renderable_type, get_settings, set_display_mode, settings_context
from dx.types import DXDisplayMode

settings = get_settings()


def test_set_display_mode(get_ipython: TerminalInteractiveShell):
    """
    Make sure calling dx.set_display_mode() properly configures the
    IPython display formatter and updates settings.
    """
    set_display_mode("plain", ipython_shell=get_ipython)
    assert settings.DISPLAY_MODE == DXDisplayMode.plain

    set_display_mode("simple", ipython_shell=get_ipython)
    assert settings.DISPLAY_MODE == DXDisplayMode.simple

    set_display_mode("enhanced", ipython_shell=get_ipython)
    assert settings.DISPLAY_MODE == DXDisplayMode.enhanced


def test_settings_context_preserves_global_setting(get_ipython: TerminalInteractiveShell):
    """
    Test that using the settings_context() context manager
    does not permanently change a global setting.
    """
    set_display_mode("simple", ipython_shell=get_ipython)
    max_rows = settings.DISPLAY_MAX_ROWS

    with settings_context(display_max_rows=1, ipython_shell=get_ipython):
        assert settings.DISPLAY_MAX_ROWS == 1

    assert settings.DISPLAY_MAX_ROWS != 1
    assert settings.DISPLAY_MAX_ROWS == max_rows, f"{settings=}"


def test_settings_context_preserves_global_display_mode(get_ipython: TerminalInteractiveShell):
    """
    Test that using the settings_context() context manager
    does not permanently change the display mode.
    """
    set_display_mode("simple", ipython_shell=get_ipython)

    with settings_context(display_mode="enhanced", ipython_shell=get_ipython):
        assert settings.DISPLAY_MODE == DXDisplayMode.enhanced, f"{settings=}"

    assert settings.DISPLAY_MODE == DXDisplayMode.simple, f"{settings=}"


def test_add_renderables():
    renderables = set(settings.RENDERABLE_OBJECTS)

    class FakeRenderable:
        pass

    add_renderable_type(FakeRenderable)
    assert settings.RENDERABLE_OBJECTS == renderables | {FakeRenderable}
