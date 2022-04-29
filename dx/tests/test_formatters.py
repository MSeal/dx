from dx.formatters import DX_MEDIA_TYPE, format_dx


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


# # TODO: mock IPython environment's display formatter

# @pytest.mark.parametrize("in_ipython_env", [True, False])
# def test_register_display_formatter(in_ipython_env: bool):
#     """
#     Test that the IPython display formatter is overridden
#     when in an IPython environment if `dx.register()` is called.
#     """
#     pass


# @pytest.mark.parametrize("in_ipython_env", [True, False])
# def test_deregister_display_formatter(in_ipython_env: bool):
#     """
#     Test that the IPython display formatter is reset to the defaults
#     when in an IPython environment if `dx.deregister()` is called.
#     """
#     pass
