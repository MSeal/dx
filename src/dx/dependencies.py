from importlib.util import find_spec

import pandas as pd
import structlog

logger = structlog.get_logger(__name__)


def package_installed(package_name) -> bool:
    package_exists = find_spec(package_name) is not None
    return package_exists


def dask_installed():
    return package_installed("dask")


def geopandas_installed():
    return package_installed("geopandas")


def modin_installed():
    return package_installed("modin")


def polars_installed():
    return package_installed("polars")


def vaex_installed():
    return package_installed("vaex")


def get_default_renderable_types() -> dict:
    """Return a dictionary of default renderable types,
    including callable functions or names of methods to use
    to convert a specific type to a pandas.DataFrame.
    """
    types = {
        pd.Series: None,
        pd.DataFrame: None,
    }

    if dask_installed():
        import dask.dataframe as dd

        dd_types = {dd.Series: "compute", dd.DataFrame: "compute"}
        types.update(dd_types)

    if geopandas_installed():
        import geopandas as gpd

        gpd_types = {gpd.GeoDataFrame: None, gpd.GeoSeries: None}
        types.update(gpd_types)

    if modin_installed():
        import modin.pandas as mpd

        mpd_types = {mpd.DataFrame: "_to_pandas", mpd.Series: "_to_pandas"}
        types.update(mpd_types)

    if polars_installed():
        import polars as pl

        pl_types = {pl.DataFrame: "to_pandas", pl.Series: "to_pandas"}
        types.update(pl_types)

    if vaex_installed():
        import vaex

        vaex_types = {vaex.dataframe.DataFrame: "to_pandas_df"}
        types.update(vaex_types)

    return types
