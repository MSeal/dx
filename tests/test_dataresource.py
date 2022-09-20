import uuid

import pytest

from dx.formatters.main import format_output, generate_body
from dx.formatters.simple import get_dataresource_settings
from dx.settings import settings_context
from dx.utils.datatypes import quick_random_dataframe

dataresource_settings = get_dataresource_settings()


def test_simple_data_structure(sample_dataframe):
    """
    The transformed data needs to represent a list of lists,
    each associated with a column in the dataframe,
    including one for the dataframe's index.
    """
    display_id = str(uuid.uuid4())
    with settings_context(display_mode="simple"):
        payload = generate_body(sample_dataframe, display_id)
    data = payload["data"]
    assert isinstance(data, list)
    assert len(data) == 3
    assert isinstance(data[0], dict)


def test_simple_data_order(sample_dataframe):
    """
    Ensure the payload contains lists as row values,
    and not column values.
    """
    display_id = str(uuid.uuid4())
    with settings_context(display_mode="simple"):
        payload = generate_body(sample_dataframe, display_id)
    data = payload["data"]
    assert data[0] == {"col_1": "a", "col_2": "b", "col_3": "c", "index": 0}
    assert data[1] == {"col_1": "a", "col_2": "b", "col_3": "c", "index": 1}
    assert data[2] == {"col_1": "a", "col_2": "b", "col_3": "c", "index": 2}


def test_fields_match_data_width(sample_dataframe):
    """
    The number of fields in the schema needs to match
    the number of dictionary keys per item in the data list.
    """
    display_id = str(uuid.uuid4())
    with settings_context(display_mode="simple"):
        payload = generate_body(sample_dataframe, display_id)
    data = payload["data"]
    fields = payload["schema"]["fields"]
    assert len(data[0]) == len(fields)


@pytest.mark.parametrize("enabled", [True, False])
def test_datalink_toggle(enabled: bool):
    """
    A dataframe with mixed types should be able to make it through
    the entire "simple" format process with datalink enabled.
    """
    df = quick_random_dataframe()
    with settings_context(enable_datalink=enabled, display_mode="simple"):
        try:
            format_output(df)
        except Exception as e:
            assert False, f"failed with {e}"
