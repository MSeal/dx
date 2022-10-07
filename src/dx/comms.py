from typing import Optional

import pandas as pd
import structlog
from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell

from dx.filtering import handle_resample
from dx.types import DEXResampleMessage

logger = structlog.get_logger(__name__)


# ref: https://jupyter-notebook.readthedocs.io/en/stable/comms.html#opening-a-comm-from-the-frontend
def resampler(comm, open_msg):
    """
    Datalink resample request.
    """

    @comm.on_msg
    def _recv(msg):
        # Is separate function to make testing easier.
        handle_resample_comm(msg)


def handle_resample_comm(msg):
    content = msg.get("content")
    if not content:
        return

    data = content.get("data")
    if not data:
        return

    if "display_id" in data and "filters" in data:
        # TODO: check for explicit resample value?
        msg = DEXResampleMessage.parse_obj(data)
        handle_resample(msg)


def renamer(comm, open_msg):
    """Rename a SQL cell dataframe."""

    @comm.on_msg
    def _recv(msg):
        handle_renaming_comm(msg)


def handle_renaming_comm(msg: dict, ipython_shell: Optional[InteractiveShell]):
    """Implementation behind renaming a SQL cell dataframe via comms"""
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

        value_to_rename = ipython_shell.user_ns.get(data["old_name"])

        # Do not rename unless old_name mapped onto exactly a dataframe.
        #
        # (Handles case when it maps onto None, indicating that the old name
        #  hasn't been assigned to at all yet (i.e. user gestured to rename
        #  SQL cell dataframe name before the SQL cell has even been run the
        #  first time yet))
        #
        if isinstance(value_to_rename, pd.DataFrame):
            # New name can be empty string, indicating to drop reference to the var.
            if data["new_name"]:
                ipython_shell.user_ns[data["new_name"]] = value_to_rename

            # But old name will always be present in message. Delete it now.
            del ipython_shell.user_ns[data["old_name"]]


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
