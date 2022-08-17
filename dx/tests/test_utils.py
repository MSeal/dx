import pandas as pd

from dx.settings import get_settings, settings_context
from dx.utils import is_default_index, normalize_index_and_columns

settings = get_settings()


def test_default_index_returns_true(sample_dataframe: pd.DataFrame):
    index = sample_dataframe.index
    assert is_default_index(index)


def test_unsorted_default_index_returns_true(sample_dataframe: pd.DataFrame):
    shuffled_sample_dataframe = sample_dataframe.sample(len(sample_dataframe))
    index = shuffled_sample_dataframe.index
    assert is_default_index(index)


def test_custom_index_returns_false(sample_dataframe: pd.DataFrame):
    sample_dataframe.set_index("col_1", inplace=True)
    index = sample_dataframe.index
    assert not is_default_index(index)


def test_multiindex_returns_false(sample_dataframe: pd.DataFrame):
    sample_dataframe.set_index(["col_1", "col_2"], inplace=True)
    index = sample_dataframe.index
    assert not is_default_index(index)


def test_default_index_persists(sample_dataframe: pd.DataFrame):
    """
    Default indexes should not be reset.
    """
    df = normalize_index_and_columns(sample_dataframe.copy())
    assert df.index.equals(sample_dataframe.index)


def test_custom_index_resets(sample_dataframe: pd.DataFrame):
    """
    Custom indexes should reset to ensure the `index` is passed
    with row value numbers to the frontend, from 0 to the length of the dataframe.
    """
    with settings_context(RESET_INDEX_VALUES=True):
        sample_dataframe.set_index(["col_1", "col_2"], inplace=True)
        assert isinstance(sample_dataframe.index, pd.MultiIndex)
        df = normalize_index_and_columns(sample_dataframe.copy())
        assert not df.index.equals(sample_dataframe.index)
        assert not isinstance(df.index, pd.MultiIndex)
