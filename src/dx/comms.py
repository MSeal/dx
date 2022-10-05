import structlog
from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell

import pandas as pd

from dx.filtering import handle_resample
from dx.types import DEXResampleMessage

logger = structlog.get_logger(__name__)


# ref: https://jupyter-notebook.readthedocs.io/en/stable/comms.html#opening-a-comm-from-the-frontend
def resampler(comm, open_msg):
    @comm.on_msg
    def _recv(msg):
        handle_comm_msg(msg)


def handle_comm_msg(msg):
    content = msg.get("content", {})
    if not content:
        return

    data = content.get("data", {})
    if not data:
        return

    data = msg["content"]["data"]

    if "display_id" in data and "filters" in data:
        # TODO: check for explicit resample value?
        msg = DEXResampleMessage.parse_obj(data)
        handle_resample(msg)


def renamer(comm, open_msg):
    @comm.on_msg
    def _recv(msg):

        content = msg.get("content", {})
        if not content:
            return

        data = content.get("data", {})
        if not data:
            return

        data = msg["content"]["data"]

        if "old_name" in data and "new_name" in data:
            shell = get_ipython()
            to_rename = shell.user_ns.get(data["old_name"])
            if isinstance(to_rename, pd.DataFrame):
                shell.user_ns[data["new_name"]] = to_rename
                del shell.user_ns[data["old_name"]]

    comm.send({"connected": True})


def register_comm(ipython_shell: InteractiveShell) -> None:
    """
    Registers the comm target function with the IPython kernel.
    """
    from dx.settings import get_settings

    if getattr(ipython_shell, "kernel", None) is None:
        # likely a TerminalInteractiveShell
        return

    if get_settings().ENABLE_DATALINK:
        ipython_shell.kernel.comm_manager.register_target("datalink", resampler)

    if get_settings().ENABLE_RENAMER:
        ipython_shell.kernel.comm_manager.register_target("rename", renamer)


if (ipython := get_ipython()) is not None:
    register_comm(ipython)
