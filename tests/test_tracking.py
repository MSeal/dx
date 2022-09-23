import pandas as pd
from IPython.terminal.interactiveshell import TerminalInteractiveShell

from dx.utils.formatting import normalize_index_and_columns
from dx.utils.tracking import DXDataFrame, generate_df_hash


def test_dxdataframe(
    sample_random_dataframe: pd.DataFrame,
    get_ipython: TerminalInteractiveShell,
):
    """
    Ensure we can create a DXDataFrame from a pandas DataFrame.
    """
    try:
        DXDataFrame(
            df=sample_random_dataframe,
            ipython_shell=get_ipython,
        )
    except Exception as e:
        assert False, f"{e}"


class TestVariableTracking:
    def test_dxdataframe_finds_variable_name(
        self,
        sample_random_dataframe: pd.DataFrame,
        get_ipython: TerminalInteractiveShell,
    ):
        """
        Test that the DXDataFrame finds the correctly-assigned
        pandas DataFrame variable name.
        """
        get_ipython.user_ns["test_df"] = sample_random_dataframe

        dxdf = DXDataFrame(
            df=sample_random_dataframe,
            ipython_shell=get_ipython,
        )
        assert dxdf.variable_name == "test_df"

    def test_dxdataframe_creates_variable_name(
        self,
        sample_random_dataframe: pd.DataFrame,
        get_ipython: TerminalInteractiveShell,
    ):
        """
        Test that the DXDataFrame creates a new temporary variable
        for dataframes that haven't been assigned within the user's
        namespace.
        """
        dxdf = DXDataFrame(
            df=sample_random_dataframe,
            ipython_shell=get_ipython,
        )
        assert dxdf.variable_name.startswith("unk_dataframe")


def test_dxdataframe_creates_hash(
    sample_random_dataframe: pd.DataFrame,
    get_ipython: TerminalInteractiveShell,
):
    """
    Test that the DXDataFrame creates a unique hash for the
    dataframe after cleaning the index and columns.
    """
    dxdf = DXDataFrame(
        df=sample_random_dataframe,
        ipython_shell=get_ipython,
    )
    clean_sample_dataframe = normalize_index_and_columns(sample_random_dataframe)
    assert dxdf.hash == generate_df_hash(clean_sample_dataframe)


def test_dxdataframe_metadata(
    sample_dxdataframe: DXDataFrame,
    sample_cleaned_random_dataframe: pd.DataFrame,
):
    """
    Test that the DXDataFrame creates metadata for the frontend
    including the appropriate dataframe information and datalink keys.
    """
    metadata = sample_dxdataframe.metadata
    assert "datalink" in metadata and "display_id" in metadata
    assert metadata["display_id"] == sample_dxdataframe.display_id
    assert metadata["datalink"]["display_id"] == sample_dxdataframe.display_id

    datalink_metadata = metadata["datalink"]

    assert "dataframe_info" in datalink_metadata
    assert (
        datalink_metadata["dataframe_info"]["orig_num_rows"]
        == sample_cleaned_random_dataframe.shape[0]
    )
    assert (
        datalink_metadata["dataframe_info"]["orig_num_cols"]
        == sample_cleaned_random_dataframe.shape[1]
    )

    assert "dx_settings" in datalink_metadata
    assert datalink_metadata["dx_settings"]

    assert isinstance(datalink_metadata["applied_filters"], list)
    assert isinstance(datalink_metadata["sample_history"], list)
