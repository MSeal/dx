import pandas as pd
from IPython import get_ipython
from IPython.core.formatters import BaseFormatter

from .dx import DATARESOURCE_MEDIA_TYPE, DX_MEDIA_TYPE


class DXSchemaFormatter(BaseFormatter):
    # FOLLOWUP: does anything need to change here?
    print_method = "_repr_data_resource_"
    _return_type = (dict,)


class TableSchemaFormatter(BaseFormatter):
    print_method = "_repr_data_resource_"
    _return_type = (dict,)


def deregister_dx_formatting(media_type: str = DX_MEDIA_TYPE) -> None:
    """Reverts IPython.display_formatter.formatters to original states"""
    pd.options.display.html.table_schema = False
    pd.options.display.max_rows = 60

    formatters = get_ipython().display_formatter.formatters
    if media_type in formatters:
        formatters.pop(media_type)

    # this should effectively be the same as using
    # `pandas.io.formats.printing.enable_data_resource_formatter(True)`,
    # except calling that directly doesn't update the IPython formatters
    formatters[DATARESOURCE_MEDIA_TYPE] = TableSchemaFormatter()
    formatters[DATARESOURCE_MEDIA_TYPE].enabled = True


def register_dx_formatter(media_type: str = DX_MEDIA_TYPE) -> None:
    """Registers a media_type for IPython display formatting"""
    pd.options.display.html.table_schema = True
    pd.options.display.max_rows = 100_000

    formatters = get_ipython().display_formatter.formatters
    formatters[media_type] = DXSchemaFormatter()
    # the default pandas `Dataframe._repl_html_` will not work correctly
    # if enabled=True here
    formatters[media_type].enabled = False


disable = deregister_dx_formatting
enable = register_dx_formatter
