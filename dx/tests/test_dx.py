import uuid

import pandas as pd

from dx.formatters.dx import format_dx, get_dx_settings
from dx.formatters.utils import is_default_index

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


def test_default_index_persists(sample_dataframe: pd.DataFrame):
    """
    Default indexes should not be reset.
    """
    payload, _ = format_dx(sample_dataframe)
    index_values = payload[dx_settings.DX_MEDIA_TYPE]["data"][0]
    assert is_default_index(pd.Index(index_values))


def test_custom_index_resets(sample_dataframe: pd.DataFrame):
    """
    Custom indexes should reset to ensure the `index` is passed
    with row value numbers to the frontend, from 0 to the length of the dataframe.
    """
    sample_dataframe.set_index(["col_1", "col_2"], inplace=True)
    payload, _ = format_dx(sample_dataframe)
    index_values = payload[dx_settings.DX_MEDIA_TYPE]["data"][0]
    assert index_values != sample_dataframe.index.tolist()
    assert is_default_index(pd.Index(index_values))
