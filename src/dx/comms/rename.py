from typing import Optional

import structlog
from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell

logger = structlog.get_logger(__name__)


def renamer(comm, open_msg):
    """Rename a SQL cell dataframe."""

    @comm.on_msg
    def _recv(msg):
        handle_renaming_comm(msg)


UNSET = object()


def handle_renaming_comm(msg: dict, ipython_shell: Optional[InteractiveShell] = None):
    """Implementation behind renaming a SQL cell output variable via comms"""
    content = msg.get("content")
    if not content:
        return

    data = content.get("data")
    if not data:
        return

    if "old_name" in data and "new_name" in data:

        if ipython_shell is None:  # noqa
            # shell will be passed in from test suite, otherwise go with global shell.
            ipython_shell = get_ipython()

        value_to_rename = ipython_shell.user_ns.get(data["old_name"], UNSET)
        if value_to_rename is not UNSET:
            # New name can be empty string, indicating to drop reference to the var.
            if data["new_name"]:
                ipython_shell.user_ns[data["new_name"]] = value_to_rename

            # But old name will always be present in message. Delete it now.
            del ipython_shell.user_ns[data["old_name"]]


def register_renamer_comm(ipython_shell: InteractiveShell) -> None:
    """
    Registers the comm target function with the IPython kernel.
    """
    from dx.settings import get_settings

    if getattr(ipython_shell, "kernel", None) is None:
        # likely a TerminalInteractiveShell
        return

    if get_settings().ENABLE_RENAMER:
        ipython_shell.kernel.comm_manager.register_target("rename", renamer)


if (ipython := get_ipython()) is not None:
    register_renamer_comm(ipython)
