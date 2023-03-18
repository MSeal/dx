from dx.settings import add_renderable_type, get_settings, set_display_mode, settings_context
from dx.types.main import DXDisplayMode

settings = get_settings()


def test_set_display_mode():
    """
    Make sure calling dx.set_display_mode() properly configures the
    IPython display formatter and updates settings.
    """
    set_display_mode("plain")
    assert settings.DISPLAY_MODE == DXDisplayMode.plain

    set_display_mode("simple")
    assert settings.DISPLAY_MODE == DXDisplayMode.simple

    set_display_mode("enhanced")
    assert settings.DISPLAY_MODE == DXDisplayMode.enhanced


def test_settings_context_preserves_global_setting():
    """
    Test that using the settings_context() context manager
    does not permanently change a global setting.
    """
    set_display_mode("simple")
    max_rows = settings.DISPLAY_MAX_ROWS

    with settings_context(display_max_rows=1):
        assert settings.DISPLAY_MAX_ROWS == 1

    assert settings.DISPLAY_MAX_ROWS != 1
    assert settings.DISPLAY_MAX_ROWS == max_rows, f"{settings=}"


def test_settings_context_preserves_global_display_mode():
    """
    Test that using the settings_context() context manager
    does not permanently change the display mode.
    """
    set_display_mode("simple")

    with settings_context(display_mode="enhanced"):
        assert settings.DISPLAY_MODE == DXDisplayMode.enhanced, f"{settings=}"

    assert settings.DISPLAY_MODE == DXDisplayMode.simple, f"{settings=}"


def test_add_renderables():
    class FakeRenderable:
        pass

    add_renderable_type(FakeRenderable)
    assert FakeRenderable in settings.get_renderable_types().keys()
