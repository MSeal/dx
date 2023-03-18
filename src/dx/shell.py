from functools import lru_cache
from typing import Optional

from ipykernel.zmqshell import ZMQInteractiveShell
from IPython import get_ipython


class Shell:
    _instance = None

    @classmethod
    def singleton(cls, ipython_shell: Optional[ZMQInteractiveShell] = None) -> ZMQInteractiveShell:
        if cls._instance is None:
            cls._instance = ipython_shell or get_ipython()
        return cls._instance


@lru_cache
def get_ipython_shell(ipython_shell: Optional[ZMQInteractiveShell] = None) -> ZMQInteractiveShell:
    """Returns the current IPython shell instance."""
    return Shell().singleton(ipython_shell=ipython_shell)
