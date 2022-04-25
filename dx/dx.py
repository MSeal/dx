import pathlib
from typing import List, Optional, Union

import pandas as pd
from IPython.display import display as ipydisplay
from pandas.io.json import build_table_schema

from .config import in_noteable_env

DX_MEDIA_TYPE = "application/vnd.dex.v1+json"
DATARESOURCE_MEDIA_TYPE = "application/vnd.dataresource+json"


class DXDataFrame(pd.DataFrame):
    """Convenience class to provide DEX-focused methods for IPython rendering"""

    _display_index = False
    media_type = DX_MEDIA_TYPE

    def display(self, media_type: Optional[str] = None, index: bool = False) -> None:
        """Render DEXDataFrame based on provided media type."""

        if not in_noteable_env():
            # TODO: should this be treated differently?
            ipydisplay(self)
            return

        media_type = media_type or self.media_type
        self._display_index = index
        payload = {
            "schema": self.table_schema,
            "data": self.data_transform(media_type=media_type),
            # "summary_statistics": {},
            # "dx-seed": {},
        }
        ipydisplay({media_type: payload}, raw=True)
        return

    def data_transform(self, media_type: str) -> List:
        """
        Transforms the current dataframe into a list of dictionaries
        or list of columnar values, depending on the media type provided.
        """
        if media_type != self.media_type:
            # use default data orient
            return self.to_dict(orient="records")

        # we can't use `.to_dict(orient='list')` here since that would return a dictionary of {column: [values]} pairs
        if self._display_index:
            return self.reset_index().transpose().values.tolist()
        return self.transpose().values.tolist()

    @property
    def table_schema(self):
        return build_table_schema(self, index=self._display_index)


def display(
    data: Union[List[dict], pd.DataFrame, Union[pathlib.Path, str]],
    media_type: Optional[str] = None,
    index: bool = False,
) -> None:
    """Convenience function to allow calling `dx.display(df)` on a pandas Dataframe, tabular data structure, or filepath."""

    # TODO: handle this in DXDataFrame init instead?
    if isinstance(data, str):
        path = pathlib.PurePosixPath(data)
        if path.suffix == ".csv":
            data = pd.read_csv(data)
        elif path.suffix == ".json":
            data = pd.read_json(data)
        else:
            raise ValueError(f"Unsupported file type: `{path.suffix}`")

    return DXDataFrame(data).display(media_type=media_type, index=index)


# backwards-compatibility
dx = display
