from dx.comms.resample import handle_resample_comm
from dx.types.filters import DEXResampleMessage


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
