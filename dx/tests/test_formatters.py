from dx.formatters import (
    DX_MEDIA_TYPE,
    DXDisplayFormatter,
    deregister,
    format_dx,
    register,
)
from IPython.core.formatters import DisplayFormatter
from IPython.terminal.interactiveshell import TerminalInteractiveShell


def test_media_type(sample_dataframe):
    payload, _ = format_dx(sample_dataframe)
    assert DX_MEDIA_TYPE in payload


def test_data_structure(sample_dataframe):
    """
    The transformed data needs to represent a list of lists,
    each associated with a column in the dataframe,
    including one for the dataframe's index.
    """
    payload, _ = format_dx(sample_dataframe)
    data = payload[DX_MEDIA_TYPE]["data"]
    assert isinstance(data, list)
    assert len(data) == 4
    assert isinstance(data[0], list)


def test_data_list_order(sample_dataframe):
    """
    Ensure the payload contains lists as column values,
    and not row values.
    """
    payload, _ = format_dx(sample_dataframe)
    data = payload[DX_MEDIA_TYPE]["data"]
    assert data[0] == [0, 1, 2]  # index values
    assert data[1] == list("aaa")  # "col_1" values
    assert data[2] == list("bbb")  # "col_2" values
    assert data[3] == list("ccc")  # "col_3" values


def test_fields_match_data_length(sample_dataframe):
    """
    The number of fields in the schema needs to match
    the number of lists in the data list.
    """
    payload, _ = format_dx(sample_dataframe)
    data = payload[DX_MEDIA_TYPE]["data"]
    fields = payload[DX_MEDIA_TYPE]["schema"]["fields"]
    assert len(data) == len(fields)


def test_register_ipython_display_formatter(get_ipython: TerminalInteractiveShell):
    """
    Test that the display formatter for an IPython shell is
    successfully registered as a DXDisplayFormatter.
    """
    register(ipython_shell=get_ipython)
    assert isinstance(get_ipython.display_formatter, DXDisplayFormatter)


def test_deregister_ipython_display_formatter(get_ipython: TerminalInteractiveShell):
    """
    Test that the display formatter reverts to the default
    `IPython.core.formatters.DisplayFormatter` after deregistering.
    """
    register(ipython_shell=get_ipython)
    assert isinstance(get_ipython.display_formatter, DXDisplayFormatter)

    deregister(ipython_shell=get_ipython)
    assert isinstance(get_ipython.display_formatter, DisplayFormatter)
