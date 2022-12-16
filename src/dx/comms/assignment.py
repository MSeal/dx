from typing import Optional

import structlog
from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell

from dx.filtering import resample_from_db
from dx.types.filters import DEXFilterSettings
from dx.utils.formatting import incrementing_label

logger = structlog.get_logger(__name__)


# ref: https://jupyter-notebook.readthedocs.io/en/stable/comms.html#opening-a-comm-from-the-frontend
def dataframe_assignment(comm, open_msg):
    """
    Datalink resample request.
    """

    @comm.on_msg
    def _recv(msg):
        # Is separate function to make testing easier.
        handle_assignment_comm(msg)

    comm.send({"status": "connected"})


def handle_assignment_comm(msg: dict, ipython_shell: Optional[InteractiveShell] = None):
    data = msg.get("content", {}).get("data", {})
    if not data:
        return

    if "display_id" in data and "variable_name" in data:
        filters = data["filters"]
        sample_size = data["sample_size"]

        sql_filter = f"SELECT * FROM {{table_name}} LIMIT {sample_size}"
        if filters:
            dex_filters = DEXFilterSettings(filters=filters)
            sql_filter_str = dex_filters.to_sql_query()
            sql_filter = f"SELECT * FROM {{table_name}} WHERE {sql_filter_str} LIMIT {sample_size}"

        sampled_df = resample_from_db(
            display_id=data["display_id"],
            sql_filter=sql_filter,
            filters=filters,
            assign_subset=False,
        )

        ipython = ipython_shell or get_ipython()
        variable_name = data["variable_name"]

        # if the variable already exists in the user namespace, add a suffix so the previous value isn't overwritten
        if variable_name in ipython.user_ns:
            variable_name = incrementing_label(variable_name, ipython.user_ns)
        logger.debug(f"assigning {len(sampled_df)}-row dataframe to `{variable_name}` in {ipython}")
        ipython.user_ns[variable_name] = sampled_df


def register_assignment_comm(ipython_shell: InteractiveShell) -> None:
    """
    Registers the comm target function with the IPython kernel.
    """
    from dx.settings import get_settings

    if get_settings().ENABLE_ASSIGNMENT:
        ipython_shell.kernel.comm_manager.register_target(
            "datalink_assignment", dataframe_assignment
        )
