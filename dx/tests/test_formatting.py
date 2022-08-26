import pandas as pd
from IPython.terminal.interactiveshell import TerminalInteractiveShell

from dx.formatters.dataresource import get_dataresource_settings, handle_dataresource_format
from dx.formatters.dx import get_dx_settings, handle_dx_format

dataresource_settings = get_dataresource_settings()
dx_settings = get_dx_settings()


def test_dataresource_media_type(
    sample_dataframe: pd.DataFrame,
    get_ipython: TerminalInteractiveShell,
):
    payload, metadata = handle_dataresource_format(sample_dataframe, ipython_shell=get_ipython)
    assert dataresource_settings.DATARESOURCE_MEDIA_TYPE in payload
    assert dataresource_settings.DATARESOURCE_MEDIA_TYPE in metadata


def test_dx_media_type(
    sample_dataframe: pd.DataFrame,
    get_ipython: TerminalInteractiveShell,
):
    payload, metadata = handle_dx_format(sample_dataframe, ipython_shell=get_ipython)
    assert dx_settings.DX_MEDIA_TYPE in payload
    assert dx_settings.DX_MEDIA_TYPE in metadata
