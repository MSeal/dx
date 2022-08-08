import pandas as pd
from IPython.core.formatters import DisplayFormatter
from IPython.terminal.interactiveshell import TerminalInteractiveShell

import dx
from dx.formatters.dataresource import DXDataResourceDisplayFormatter
from dx.formatters.dx import DXDisplayFormatter
from dx.settings import get_settings, set_display_mode
from dx.types import DXDisplayMode

settings = get_settings()


def test_set_display_mode(get_ipython: TerminalInteractiveShell):
    """
    Make sure calling dx.set_display_mode() properly configures the
    IPython display formatter and updates settings.
    """
    set_display_mode("plain", ipython_shell=get_ipython)
    assert settings.DISPLAY_MODE == DXDisplayMode.plain
    assert isinstance(get_ipython.display_formatter, DisplayFormatter)

    set_display_mode("simple", ipython_shell=get_ipython)
    assert settings.DISPLAY_MODE == DXDisplayMode.simple
    assert isinstance(get_ipython.display_formatter, DXDataResourceDisplayFormatter)

    set_display_mode("enhanced", ipython_shell=get_ipython)
    assert settings.DISPLAY_MODE == DXDisplayMode.enhanced
    assert isinstance(get_ipython.display_formatter, DXDisplayFormatter)


def test_display_preserves_global_display_mode(
    get_ipython: TerminalInteractiveShell,
    sample_dataframe: pd.DataFrame,
):
    """
    Test that calling dx.display(df, mode=X) does not permanently change
    the global display mode to X.
    """
    set_display_mode("simple", ipython_shell=get_ipython)
    assert settings.DISPLAY_MODE == DXDisplayMode.simple
    assert isinstance(get_ipython.display_formatter, DXDataResourceDisplayFormatter)

    dx.display(
        sample_dataframe,
        mode=DXDisplayMode.enhanced,
        ipython_shell=get_ipython,
    )
    assert settings.DISPLAY_MODE == DXDisplayMode.simple, f"{settings=}"
