import random
from typing import Optional

import numpy as np
import pandas as pd
import structlog

try:
    import geopandas as gpd
    import shapely.geometry.base
    from shapely.geometry import mapping

    GEOPANDAS_INSTALLED = True
except ImportError:
    GEOPANDAS_INSTALLED = False

logger = structlog.get_logger(__name__)


def handle_geometry_series(s: pd.Series):
    """
    Converts shapely.geometry values to JSON.
    """
    if not GEOPANDAS_INSTALLED:
        return s

    types = (
        shapely.geometry.base.BaseGeometry,
        shapely.geometry.base.BaseMultipartGeometry,
    )
    if any(isinstance(v, types) for v in s.values):
        logger.debug(f"series `{s.name}` has geometries; converting to JSON")
        s = s.apply(lambda x: x.to_json() if isinstance(x, types) else x)
    return s


def generate_latlon_series(num_rows: int):
    if not GEOPANDAS_INSTALLED:
        logger.warning("geopandas is not installed, skipping generate_latlon_series")
        return np.nan

    lats = [random.randint(-90, 89) + np.random.rand() for _ in range(num_rows)]
    lons = [random.randint(-180, 179) + np.random.rand() for _ in range(num_rows)]
    return gpd.points_from_xy(lons, lats)


def generate_filled_geojson_series(
    num_rows: int,
    existing_latlon_series: Optional[pd.Series] = None,
):
    if not GEOPANDAS_INSTALLED:
        logger.warning("geopandas is not installed, skipping filled_geojson_column")
        return np.nan

    if existing_latlon_series is None:
        latlon_series = generate_latlon_series(num_rows)
    else:
        latlon_series = existing_latlon_series
    buffer_series = gpd.GeoSeries(latlon_series).apply(lambda x: x.buffer(np.random.rand()))
    return gpd.GeoSeries(buffer_series).apply(mapping)


def generate_exterior_bounds_geojson_series(
    num_rows: int,
    existing_latlon_series: Optional[pd.Series] = None,
):
    if not GEOPANDAS_INSTALLED:
        logger.warning("geopandas is not installed, skipping exterior_geojson_column")
        return np.nan

    if existing_latlon_series is None:
        latlon_series = generate_latlon_series(num_rows)
    else:
        latlon_series = existing_latlon_series

    envelope_series = gpd.GeoSeries(latlon_series).apply(
        lambda x: x.buffer(np.random.rand()).envelope.exterior
    )
    return gpd.GeoSeries(envelope_series).apply(mapping)
