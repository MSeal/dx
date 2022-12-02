import structlog
from IPython.core.interactiveshell import InteractiveShell

from dx.filtering import handle_resample
from dx.types.filters import DEXResampleMessage

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
    data = msg.get("content", {}).get("data", {})
    if not data:
        return

    if "display_id" in data and "filters" in data:
        msg = DEXResampleMessage.parse_obj(data)
        handle_resample(msg)


def register_resampler_comm(ipython_shell: InteractiveShell) -> None:
    """
    Registers the comm target function with the IPython kernel.
    """
    from dx.settings import get_settings

    if getattr(ipython_shell, "kernel", None) is None:
        # likely a TerminalInteractiveShell
        return

    if get_settings().ENABLE_DATALINK:
        ipython_shell.kernel.comm_manager.register_target("datalink_resample", resampler)
