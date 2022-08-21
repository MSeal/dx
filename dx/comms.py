import structlog
from IPython import get_ipython

logger = structlog.get_logger(__name__)


# ref: https://jupyter-notebook.readthedocs.io/en/stable/comms.html#opening-a-comm-from-the-frontend
def target_func(comm, open_msg):
    @comm.on_msg
    def _recv(msg):
        from dx.filtering import update_display_id

        data = msg["content"]["data"]
        if "display_id" in data:
            update_display_id(
                display_id=data["display_id"],
                pandas_filter=data.get("pandas_filter"),
                sql_filter=data.get("sql_filter"),
                filters=data.get("filters"),
                output_variable_name=data.get("output_variable_name"),
                limit=data["limit"],
            )

    comm.send({"connected": True})


ipython_shell = get_ipython()
if ipython_shell is not None and getattr(ipython_shell, "kernel", None):
    COMM_MANAGER = ipython_shell.kernel.comm_manager
    COMM_MANAGER.register_target("datalink", target_func)
