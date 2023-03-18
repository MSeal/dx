import pathlib
from typing import List, Union

import pandas as pd
from IPython import display as ipydisplay

from dx.formatters.main import handle_format
from dx.settings import settings_context
from dx.types.main import DXDisplayMode


def display(
    data: Union[List[dict], pd.DataFrame, Union[pathlib.Path, str]],
    mode: DXDisplayMode = DXDisplayMode.simple,
    **kwargs,
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
    with settings_context(display_mode=mode):
        handle_format(df, **kwargs)


def show_docs(
    src: str = "https://noteable-io.github.io/dx/",
    width: str = "100%",
    height: str = "400px",
) -> None:
    """Renders the dx documentation in an IFrame for use in a notebook environment."""
    docs_iframe = ipydisplay.IFrame(src=src, width=width, height=height)
    ipydisplay.display(docs_iframe)
