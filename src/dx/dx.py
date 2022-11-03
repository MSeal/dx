import pathlib
from typing import List, Optional, Union

import pandas as pd
from IPython.core.interactiveshell import InteractiveShell

from dx.formatters.main import handle_format
from dx.settings import settings_context
from dx.types import DXDisplayMode


def display(
    data: Union[List[dict], pd.DataFrame, Union[pathlib.Path, str]],
    mode: DXDisplayMode = DXDisplayMode.simple,
    ipython_shell: Optional[InteractiveShell] = None,
    **kwargs
) -> None:
    """
    Display a single object with the DX display format.
    (e.g. pd.DataFrame, .csv/.json filepath, or tabular dataset)
    """

    if isinstance(data, str):
        path = pathlib.PurePosixPath(data)
        if path.suffix == ".csv":
            data = pd.read_csv(data)
        elif path.suffix == ".json":
            data = pd.read_json(data)
        else:
            raise ValueError(f"Unsupported file type: `{path.suffix}`")

    df = pd.DataFrame(data)
    with settings_context(display_mode=mode, ipython_shell=ipython_shell):
        handle_format(df, **kwargs)

    return


# backwards-compatibility
dx = display
