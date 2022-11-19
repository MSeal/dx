from IPython import get_ipython

from .comms import *
from .datatypes import *
from .dx import *
from .formatters import *
from .loggers import *
from .plotting import *
from .settings import *
from .utils import *

__version__ = "1.3.0"

configure_logging()
set_display_mode("simple")

if (ipython := get_ipython()) is not None:
    if getattr(ipython, "kernel", None) is not None:
        register_resampler_comm(ipython)
        register_renamer_comm(ipython)
        register_assignment_comm(ipython)
