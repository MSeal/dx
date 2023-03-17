import dask.dataframe as dd
import geopandas as gpd
import modin.pandas as mpd
import pandas as pd
import polars as pl
import pytest
import vaex
from IPython.terminal.interactiveshell import TerminalInteractiveShell

from dx.formatters.main import handle_format
from dx.settings import get_settings, settings_context
from dx.utils.formatting import to_dataframe
from dx.utils.tracking import DXDF_CACHE

settings = get_settings()


def sample_dask_dataframe():
    return dd.from_pandas(pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}), npartitions=2)


def sample_geopandas_geodataframe():
    return gpd.GeoDataFrame(
        {"col1": [1, 2], "col2": [3, 4]}, geometry=gpd.points_from_xy([1, 2], [3, 4])
    )


def sample_modin_dataframe():
    return mpd.DataFrame({"col1": [1, 2], "col2": [3, 4]})


def sample_polars_dataframe():
    return pl.DataFrame({"col1": [1, 2], "col2": [3, 4]})


def sample_vaex_dataframe():
    return vaex.from_arrays(col1=[1, 2], col2=[3, 4])


DATAFRAME_TYPES = ["dask", "geopandas", "modin", "polars", "vaex"]


class TestRenderableTypes:
    @pytest.mark.parametrize("renderable_type", DATAFRAME_TYPES)
    @pytest.mark.parametrize("datalink_enabled", [True, False])
    @pytest.mark.parametrize("display_mode", ["simple", "enhanced"])
    def test_non_pandas_dataframes(
        self,
        renderable_type: str,
        display_mode: str,
        datalink_enabled: bool,
        get_ipython: TerminalInteractiveShell,
    ):
        """
        Test formatting a supported renderable data type that isn't a pandas DataFrame,
        to include the additional processing and tracking handled for datalink.

        Additionally, if datalink is enabled, ensure that the display ID was
        generated within the DXDataFrame and stored in the DXDF_CACHE.
        """
        if renderable_type == "dask":
            obj = sample_dask_dataframe()
        elif renderable_type == "geopandas":
            obj = sample_geopandas_geodataframe()
        elif renderable_type == "modin":
            obj = sample_modin_dataframe()
        elif renderable_type == "polars":
            obj = sample_polars_dataframe()
        elif renderable_type == "vaex":
            obj = sample_vaex_dataframe()

        df = to_dataframe(obj)
        assert isinstance(df, pd.DataFrame)

        # check structure after converting to dataframe
        # to make sure we didn't lose any rows/columns/etc
        assert len(df.columns) == len(obj.columns)

        if renderable_type in ["dask"]:
            assert len(df) == len(obj.compute())
        else:
            assert len(df) == len(obj)

        if hasattr(obj, "index"):
            assert list(df.index) == list(obj.index)

        try:
            with settings_context(enable_datalink=datalink_enabled, display_mode=display_mode):
                _, metadata = handle_format(df, ipython_shell=get_ipython)
                if datalink_enabled:
                    display_id = metadata[settings.MEDIA_TYPE]["display_id"]
                    assert display_id in DXDF_CACHE
        except Exception as e:
            assert False, f"{e}"
