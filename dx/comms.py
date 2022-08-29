import logging

import structlog
from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell

from dx.filtering import handle_resample

logger = structlog.get_logger(__name__)


def log(msg: str, level: int = logging.DEBUG):
    """
    Log a message to the DX logger.
    """
    logger.log(level, msg)


# ref: https://jupyter-notebook.readthedocs.io/en/stable/comms.html#opening-a-comm-from-the-frontend
def target_func(comm, open_msg):
    @comm.on_msg
    def _recv(msg):

        content = msg.get("content", {})
        if not content:
            log(f"no 'content' in {msg=}", logging.DEBUG)
            return

        data = content.get("data", {})
        if not data:
            log(f"no 'data' in {msg['data']=}", logging.DEBUG)
            return

        data = msg["content"]["data"]

        if "display_id" in data and "filters" in data:
            # TODO: check for explicit resample value?
            handle_resample(data)

    comm.send({"connected": True})


def register_comm(ipython_shell: InteractiveShell) -> None:
    """
    Registers the comm target function with the IPython kernel.
    """
    from dx.settings import get_settings

    if not get_settings().ENABLE_DATALINK:
        return

    ipython_shell.kernel.comm_manager.register_target("datalink", target_func)


if (ipython := get_ipython()) is not None:
    register_comm(ipython)
