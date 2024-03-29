import uuid

import pytest

from dx.datatypes.main import quick_random_dataframe
from dx.formatters.enhanced import get_dx_settings
from dx.formatters.main import format_output, generate_body
from dx.settings import settings_context

dx_settings = get_dx_settings()


def test_data_structure(sample_dataframe):
    """
    The transformed data needs to represent a list of lists,
    each associated with a column in the dataframe,
    including one for the dataframe's index.
    """
    display_id = str(uuid.uuid4())
    with settings_context(display_mode="enhanced"):
        payload = generate_body(sample_dataframe, display_id)
    data = payload["data"]
    assert isinstance(data, list)
    assert len(data) == 4
    assert isinstance(data[0], list)


def test_data_list_order(sample_dataframe):
    """
    Ensure the payload contains lists as column values,
    and not row values.
    """
    display_id = str(uuid.uuid4())
    with settings_context(display_mode="enhanced"):
        payload = generate_body(sample_dataframe, display_id)
    data = payload["data"]
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
    with settings_context(display_mode="enhanced"):
        payload = generate_body(sample_dataframe, display_id)
    data = payload["data"]
    fields = payload["schema"]["fields"]
    assert len(data) == len(fields)


@pytest.mark.parametrize("enabled", [True, False])
def test_datalink_toggle(enabled: bool):
    """
    A dataframe with mixed types should be able to make it through
    the entire "enhanced" format process with datalink enabled.
    """
    df = quick_random_dataframe()
    with settings_context(enable_datalink=enabled, display_mode="enhanced"):
        try:
            format_output(df)
        except Exception as e:
            assert False, f"failed with {e}"
