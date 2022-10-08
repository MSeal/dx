from dx.comms.resample import handle_resample_comm
from dx.types import DEXResampleMessage


def test_handle_resample_comm(mocker):
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
    mock_handle_resample = mocker.patch("dx.comms.handle_resample")
    handle_resample_comm(msg)
    resample_msg = DEXResampleMessage.parse_obj(msg["content"]["data"])
    mock_handle_resample.assert_called_once_with(resample_msg)


def test_handle_resample_comm_skipped(mocker):
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
    handle_resample_comm(msg)
    mock_handle_resample.assert_not_called()
