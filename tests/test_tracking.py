import duckdb
import pandas as pd

from dx.formatters.main import handle_format
from dx.settings import settings_context
from dx.shell import get_ipython_shell
from dx.utils.formatting import normalize_index_and_columns
from dx.utils.tracking import DXDataFrame, generate_df_hash


def test_dxdataframe(
    sample_random_dataframe: pd.DataFrame,
):
    """
    Ensure we can create a DXDataFrame from a pandas DataFrame.
    """
    try:
        DXDataFrame(df=sample_random_dataframe)
    except Exception as e:
        assert False, f"{e}"


class TestVariableTracking:
    def test_dxdataframe_finds_variable_name(
        self,
        sample_random_dataframe: pd.DataFrame,
    ):
        """
        Test that the DXDataFrame finds the correctly-assigned
        pandas DataFrame variable name.
        """
        get_ipython_shell().user_ns["test_df"] = sample_random_dataframe
        dxdf = DXDataFrame(df=sample_random_dataframe)
        assert dxdf.variable_name == "test_df"

    def test_dxdataframe_creates_variable_name(self, sample_random_dataframe: pd.DataFrame):
        """
        Test that the DXDataFrame creates a new temporary variable
        for dataframes that haven't been assigned within the user's
        namespace.
        """
        dxdf = DXDataFrame(df=sample_random_dataframe)
        assert dxdf.variable_name.startswith("unk_dataframe")


def test_dxdataframe_creates_hash(sample_random_dataframe: pd.DataFrame):
    """
    Test that the DXDataFrame creates a unique hash for the
    dataframe after cleaning the index and columns.
    """
    dxdf = DXDataFrame(df=sample_random_dataframe)
    clean_sample_dataframe = normalize_index_and_columns(sample_random_dataframe)
    assert dxdf.hash == generate_df_hash(clean_sample_dataframe)


def test_dxdataframe_metadata(sample_dxdataframe: DXDataFrame):
    """
    Test that the DXDataFrame creates metadata for the frontend
    including the appropriate dataframe information and datalink keys.

    (Similar to ./test_formatting.py::TestMetadataStructure)
    """
    metadata = sample_dxdataframe.metadata
    assert "datalink" in metadata and "display_id" in metadata
    assert metadata["display_id"] == sample_dxdataframe.display_id
    assert metadata["datalink"]["display_id"] == sample_dxdataframe.display_id


def test_store_in_db(
    mocker,
    sample_random_dataframe: pd.DataFrame,
    sample_db_connection: duckdb.DuckDBPyConnection,
):
    """
    Ensure dataframes are stored as tables using the kernel's
    local database connection.
    """
    mocker.patch("dx.formatters.main.db_connection", sample_db_connection)

    get_ipython_shell().user_ns["test_df"] = sample_random_dataframe

    with settings_context(enable_datalink=True):
        handle_format(sample_random_dataframe)

    resp = sample_db_connection.execute("SELECT COUNT(*) FROM test_df").fetchone()
    assert resp[0] == len(sample_random_dataframe)
