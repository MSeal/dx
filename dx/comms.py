from IPython import get_ipython

from dx.config import IN_IPYTHON_ENV
from dx.loggers import get_logger

logger = get_logger(__name__)


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
                output_variable_name=data.get("output_variable_name"),
                limit=data["limit"],
            )

    # no idea where this goes
    comm.send({"connected": True})


ipython_shell = get_ipython()
if IN_IPYTHON_ENV and getattr(ipython_shell, "kernel", None):
    COMM_MANAGER = ipython_shell.kernel.comm_manager
    COMM_MANAGER.register_target("datalink", target_func)
