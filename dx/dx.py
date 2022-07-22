import pathlib
from typing import List, Union

import pandas as pd
from IPython.display import display as ipydisplay

from dx.settings import set_display_mode, settings
from dx.types import DXDisplayMode


def display(
    data: Union[List[dict], pd.DataFrame, Union[pathlib.Path, str]],
    mode: DXDisplayMode = DXDisplayMode.simple,
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

    orig_mode = settings.DISPLAY_MODE
    set_display_mode(mode)
    ipydisplay(df)
    set_display_mode(orig_mode)
    return


# backwards-compatibility
dx = display
