from dx.comms import handle_comm_msg
from dx.types import DEXResampleMessage


def test_handle_comm_msg(mocker):
    """
    Test that `handle_resample` is called with the correctly
    formatted resample message type if the comm receives
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
    mock_handle_resample = mocker.patch("dx.comms.handle_resample")
    handle_comm_msg(msg)
    resample_msg = DEXResampleMessage.parse_obj(msg["content"]["data"])
    mock_handle_resample.assert_called_once_with(resample_msg)


def test_handle_comm_msg_skipped(mocker):
    """
    Test that `handle_resample` is not called with invalid data.
    """
    msg = {
        "content": {
            "data": {
                "display_id": "test",
            }
        }
    }
    mock_handle_resample = mocker.patch("dx.comms.handle_resample")
    handle_comm_msg(msg)
    mock_handle_resample.assert_not_called()
