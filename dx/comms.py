import structlog
from IPython import get_ipython

from dx.settings import get_settings
from dx.types import DEXFilterSettings

settings = get_settings()
logger = structlog.get_logger(__name__)


# ref: https://jupyter-notebook.readthedocs.io/en/stable/comms.html#opening-a-comm-from-the-frontend
def target_func(comm, open_msg):
    @comm.on_msg
    def _recv(msg):
        from dx.filtering import update_display_id

        data = msg["content"]["data"]
        # should look like this:
        # {
        #     "display_id": "1c1c8b40-f1f4-4205-931d-644a42e8232d",
        #     "sampling": {
        #         "filters": [
        #             {
        #                 "column": "float_column",
        #                 "type": "METRIC_FILTER",
        #                 "predicate": "between",
        #                 "value": [0.5346270287577823, 0.673002123739554],
        #             }
        #         ],
        #     },
        #     "sample_size": 10000,
        #     "status": "submitted",
        # }

        raw_dex_filters = data["sampling"]["filters"]
        sample_size = data["sampling"]["sample_size"]
        update_params = {
            "display_id": data["display_id"],
            "sql_query": f"SELECT * FROM {{table_name}} LIMIT {sample_size}",
            "filters": raw_dex_filters,
            "limit": sample_size,
        }

        if raw_dex_filters:
            dex_filters = DEXFilterSettings(filters=raw_dex_filters)
            # used to give a pandas query string to the user
            pandas_filter_str = dex_filters.to_pandas_query()
            # used to actually filter the data
            sql_filter_str = dex_filters.to_sql_query()
            update_params.update(
                {
                    "pandas_filter": pandas_filter_str,
                    "sql_filter": f"SELECT * FROM {{table_name}} WHERE {sql_filter_str} LIMIT {sample_size}",
                    "filters": raw_dex_filters,
                }
            )

        update_display_id(**update_params)

    comm.send({"connected": True})


ipython_shell = get_ipython()
if (
    ipython_shell is not None
    and getattr(ipython_shell, "kernel", None)
    and settings.ENABLE_DATALINK
):
    COMM_MANAGER = ipython_shell.kernel.comm_manager
    COMM_MANAGER.register_target("datalink", target_func)
