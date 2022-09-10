import uuid

import numpy as np
import pandas as pd
import pytest

from dx.formatters.dataresource import (
    format_dataresource,
    generate_dataresource_body,
    get_dataresource_settings,
)
from dx.settings import settings_context
from dx.utils.datatypes import quick_random_dataframe

dataresource_settings = get_dataresource_settings()


def test_data_structure(sample_dataframe):
    """
    The transformed data needs to represent a list of lists,
    each associated with a column in the dataframe,
    including one for the dataframe's index.
    """
    display_id = str(uuid.uuid4())
    payload = generate_dataresource_body(sample_dataframe, display_id)
    data = payload["data"]
    assert isinstance(data, list)
    assert len(data) == 3
    assert isinstance(data[0], dict)


def test_data_list_order(sample_dataframe):
    """
    Ensure the payload contains lists as row values,
    and not column values.
    """
    display_id = str(uuid.uuid4())
    payload = generate_dataresource_body(sample_dataframe, display_id)
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
    payload = generate_dataresource_body(sample_dataframe, display_id)
    data = payload["data"]
    fields = payload["schema"]["fields"]
    assert len(data[0]) == len(fields)


@pytest.mark.parametrize("enabled", [True, False])
def test_datalink_toggle(enabled: bool):
    df = quick_random_dataframe()
    with settings_context(enable_datalink=enabled):
        try:
            format_dataresource(df)
        except Exception as e:
            assert False, f"failed with {e}"


@pytest.mark.parametrize("null_value", [np.nan, pd.NA])
def test_dx_converts_na_to_none(
    get_ipython: TerminalInteractiveShell,
    null_value,
):
    """
    Test dataresource formatting properly converts `pd.NA` and `NaN`
    values to `None` before passing along the payload.
    """
    df = pd.DataFrame({
        "foo": [1, 2, null_value],
        "bar": ["a", null_value, "b"],
    })
    payload = generate_dataresource_body(sample_dataframe)
    assert payload["data"][0] == {"index": 0, "foo": 1, "bar": "a"}
    assert payload["data"][1] == {"index": 1, "foo": 2, "bar": None}
    assert payload["data"][2] == {"index": 2, "foo": None, "bar": "b"}
