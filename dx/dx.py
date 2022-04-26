import pathlib
from typing import List, Union

import pandas as pd
from IPython.display import display as ipydisplay

from .formatters import format_dx


def display(
    data: Union[List[dict], pd.DataFrame, Union[pathlib.Path, str]],
) -> None:
    """
    Display a single object (pd.DataFrame, .csv/.json filepath, or tabular dataset) with the DX display format.
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
    payload, _ = format_dx(df)
    ipydisplay(payload, raw=True)
    return


# backwards-compatibility
dx = display
