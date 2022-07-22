import uuid

from dx.formatters.dx import format_dx, get_dx_settings

dx_settings = get_dx_settings()


def test_media_type(sample_dataframe):
    display_id = str(uuid.uuid4())
    payload, _ = format_dx(sample_dataframe, display_id)
    assert dx_settings.DX_MEDIA_TYPE in payload


def test_data_structure(sample_dataframe):
    """
    The transformed data needs to represent a list of lists,
    each associated with a column in the dataframe,
    including one for the dataframe's index.
    """
    display_id = str(uuid.uuid4())
    payload, _ = format_dx(sample_dataframe, display_id)
    data = payload[dx_settings.DX_MEDIA_TYPE]["data"]
    assert isinstance(data, list)
    assert len(data) == 4
    assert isinstance(data[0], list)


def test_data_list_order(sample_dataframe):
    """
    Ensure the payload contains lists as column values,
    and not row values.
    """
    display_id = str(uuid.uuid4())
    payload, _ = format_dx(sample_dataframe, display_id)
    data = payload[dx_settings.DX_MEDIA_TYPE]["data"]
    assert data[0] == [0, 1, 2]  # index values
    assert data[1] == list("aaa")  # "col_1" values
    assert data[2] == list("bbb")  # "col_2" values
    assert data[3] == list("ccc")  # "col_3" values


def test_fields_match_data_length(sample_dataframe):
    """
    The number of fields in the schema needs to match
    the number of lists in the data list.
    """
    display_id = str(uuid.uuid4())
    payload, _ = format_dx(sample_dataframe, display_id)
    data = payload[dx_settings.DX_MEDIA_TYPE]["data"]
    fields = payload[dx_settings.DX_MEDIA_TYPE]["schema"]["fields"]
    assert len(data) == len(fields)
