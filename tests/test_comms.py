import uuid

import pandas as pd
from IPython.terminal.interactiveshell import TerminalInteractiveShell

from dx.comms.assignment import handle_assignment_comm
from dx.comms.resample import handle_resample_comm
from dx.types.filters import DEXFilterSettings, DEXResampleMessage


class TestResampleComm:
    def test_resample_handled(self, mocker):
        """
        Test that `handle_resample` is called with the correctly
        formatted resample message type if the comm (`handle_resample_comm`) receives
        the right data structure.
        """
        msg = {
            "content": {
                "data": {
                    "display_id": "test",
                    "filters": [
                        {
                            "type": "METRIC_FILTER",
                            "value": [0, 1],
                            "column": "test_column",
                            "predicate": "between",
                        }
                    ],
                }
            }
        }
        mock_handle_resample = mocker.patch("dx.comms.resample.handle_resample")
        handle_resample_comm(msg)
        resample_msg = DEXResampleMessage.parse_obj(msg["content"]["data"])
        mock_handle_resample.assert_called_once_with(resample_msg)


class TestAssignmentComm:
    def test_assignment_handled(
        self,
        mocker,
        get_ipython: TerminalInteractiveShell,
        sample_dataframe: pd.DataFrame,
    ):
        """
        Test that a valid message handled through the assignment comm
        will call resample_from_db() with the provided display_id, filters,
        and sample size, and will assign a valid pandas DataFrame in the
        kernel namespace with the provided variable name.
        """
        display_id = str(uuid.uuid4())
        sample_size = 50
        msg = {
            "content": {
                "data": {
                    "cell_id": "cell1",
                    "display_id": display_id,
                    "filters": [],
                    "sample_size": sample_size,
                    "variable_name": "new_df",
                }
            }
        }
        mock_resample = mocker.patch(
            "dx.comms.assignment.resample_from_db", return_value=sample_dataframe
        )
        handle_assignment_comm(msg, ipython_shell=get_ipython)
        resample_params = {
            "display_id": display_id,
            "sql_filter": f"SELECT * FROM {{table_name}} LIMIT {sample_size}",
            "filters": [],
            "assign_subset": False,
        }
        mock_resample.assert_called_once_with(**resample_params)
        assert "new_df" in get_ipython.user_ns
        assert isinstance(get_ipython.user_ns["new_df"], pd.DataFrame)
        assert get_ipython.user_ns["new_df"].equals(sample_dataframe)

    def test_assignment_handled_with_filters(
        self,
        mocker,
        get_ipython: TerminalInteractiveShell,
        sample_dataframe: pd.DataFrame,
        sample_dex_metric_filter: dict,
    ):
        """
        Test that a valid message handled through the assignment comm
        will call resample_from_db() with the provided display_id, filters,
        and sample size, and will assign a valid pandas DataFrame in the
        kernel namespace with the provided variable name.
        """
        display_id = str(uuid.uuid4())
        sample_size = 50

        filters = [sample_dex_metric_filter]
        dex_filters = DEXFilterSettings(filters=filters)
        sql_filter = (
            f"SELECT * FROM {{table_name}} WHERE {dex_filters.to_sql_query()} LIMIT {sample_size}"
        )

        msg = {
            "content": {
                "data": {
                    "cell_id": "cell1",
                    "display_id": display_id,
                    "filters": filters,
                    "sample_size": sample_size,
                    "variable_name": "new_df",
                }
            }
        }
        mock_resample = mocker.patch(
            "dx.comms.assignment.resample_from_db", return_value=sample_dataframe
        )
        handle_assignment_comm(msg, ipython_shell=get_ipython)
        resample_params = {
            "display_id": display_id,
            "sql_filter": sql_filter,
            "filters": filters,
            "assign_subset": False,
        }
        mock_resample.assert_called_once_with(**resample_params)
        assert "new_df" in get_ipython.user_ns
        assert isinstance(get_ipython.user_ns["new_df"], pd.DataFrame)

    def test_assignment_handled_with_existing_variable(
        self,
        mocker,
        get_ipython: TerminalInteractiveShell,
        sample_dataframe: pd.DataFrame,
    ):
        """
        Test that a valid assignment message attempting to assign to an existing
        variable will be appended with a numeric suffix and will not
        affect the original variable.
        """
        existing_dataframe_variable = pd.DataFrame({"test": [1, 2, 3]})
        get_ipython.user_ns["df"] = existing_dataframe_variable

        display_id = str(uuid.uuid4())
        sample_size = 50
        msg = {
            "content": {
                "data": {
                    "cell_id": "cell1",
                    "display_id": display_id,
                    "filters": [],
                    "sample_size": sample_size,
                    "variable_name": "df",
                }
            }
        }
        mock_resample = mocker.patch(
            "dx.comms.assignment.resample_from_db", return_value=sample_dataframe
        )
        handle_assignment_comm(msg, ipython_shell=get_ipython)
        resample_params = {
            "display_id": display_id,
            "sql_filter": f"SELECT * FROM {{table_name}} LIMIT {sample_size}",
            "filters": [],
            "assign_subset": False,
        }
        mock_resample.assert_called_once_with(**resample_params)

        # new variable should be assigned with a numeric suffix
        assert "df_1" in get_ipython.user_ns
        assert isinstance(get_ipython.user_ns["df_1"], pd.DataFrame)
        assert get_ipython.user_ns["df_1"].equals(sample_dataframe)

        # old variable should still exist
        assert "df" in get_ipython.user_ns
        assert get_ipython.user_ns["df"].equals(existing_dataframe_variable)

    def test_assignment_skipped(
        self,
        mocker,
        get_ipython: TerminalInteractiveShell,
    ):
        """
        Test that variable assignment is skipped if `display_id` and
        `variable_name` are not provided in the comm message.
        """
        msg = {
            "content": {
                "data": {
                    "cell_id": "cell1",
                    "filters": [],
                    "sample_size": 50,
                    "variable_name": "new_df",
                }
            }
        }
        mock_resample = mocker.patch("dx.comms.assignment.resample_from_db")
        handle_assignment_comm(msg, ipython_shell=get_ipython)
        mock_resample.assert_not_called()
        assert "new_df" not in get_ipython.user_ns
