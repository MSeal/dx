from typing import List, Optional

from pydantic.color import Color

from dx.plotting.utils import handle_view, raise_for_missing_columns
from dx.types.charts import options
from dx.types.charts.choropleth import DEXChoroplethChartView
from dx.types.charts.tilemap import DEXTilemapChartView

__all__ = ["choropleth", "tilemap"]


def sample_choropleth(df, **kwargs) -> Optional[DEXChoroplethChartView]:
    return handle_view(df, chart_mode="choropleth", **kwargs)


def choropleth(df, **kwargs) -> Optional[DEXChoroplethChartView]:
    # TODO: define user-facing arguments and add documentation
    return sample_choropleth(df, **kwargs)


def sample_tilemap(df, **kwargs) -> Optional[DEXTilemapChartView]:
    return handle_view(df, chart_mode="tilemap", **kwargs)


def tilemap(
    df,
    lat: str,
    lon: str,
    icon_opacity: float = 1.0,
    icon_size: int = 2,
    icon_size_scale: options.DEXScale = "linear",
    stroke_color: Color = "#000000",
    stroke_width: int = 2,
    label_column: Optional[str] = None,
    tile_layer: str = "streets",
    hover_cols: Optional[List[str]] = None,
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXTilemapChartView]:
    """
    Generates a DEX tilemap from the given DataFrame.

    Parameters
    ----------
    df: pd.DataFrame
        The DataFrame to plot.
    lat: str
        The column to use for the latitude values.
    lon: str
        The column to use for the longitude values.
    icon_opacity: float
        The opacity to use for the icon (`0.0` to `1.0`)
    icon_size: Union[int, str]
        Either:
        - int: a fixed size to use for the icon (`0` to `10`)
        - str: a column name to use for functional sizing
    icon_size_scale: DEXScale
        The scale to use for functional sizing (`"linear"` or `"log"`)
    stroke_color: Color
        The color to use for the icon stroke.
    stroke_width: int
        The width to use for the icon stroke.
    tile_layer: str
        The type of tile layer to use. One of `"streets"`, `"outdoors"`, `"light"`, `"dark"`, or `"satellite"`
    return_view: bool
        Whether to return a `DEXView` object instead of render.
    **kwargs
        Additional keyword arguments to pass to the view metadata.
    """
    raise_for_missing_columns([lat, lon], df.columns)

    if isinstance(hover_cols, str):
        hover_cols = [hover_cols]
    if hover_cols is None:
        hover_cols = df.columns
    else:
        raise_for_missing_columns(hover_cols, df.columns)

    if label_column is not None:
        raise_for_missing_columns(label_column, df.columns)

    if isinstance(icon_size, str):
        # referencing a column, treat as functional sizing

        if icon_size not in df.columns:
            # "index" was chosen but isn't in columns, which passes raise_for_missing_columns()
            series = df.index
        else:
            series = df[icon_size]

        series_min = series.min()
        if str(icon_size_scale).lower() == "log":
            series_min = 1

        point_size_opts = {
            "mode": "functional",
            "size": 2,
            "met": icon_size,
            "scale": icon_size_scale,
            "min": series_min,
            "max": series.max(),
            "sizeMin": 1,
            "sizeMax": 10,
        }
    elif isinstance(icon_size, int):
        # fixed sizing, shouldn't matter what we put in here
        point_size_opts = {
            "mode": "fixed",
            "size": icon_size,
            "met": str(lon),
            "scale": icon_size_scale,
            "min": df[str(lon)].min(),
            "max": df[str(lon)].max(),
            "sizeMin": 1,
            "sizeMax": 10,
        }
    else:
        raise ValueError(f"`{type(icon_size)}` is not a valid type for `icon_size`.")

    # determine which columns are numeric and which ones are strings/mixed/etc
    dimension_cols = [col for col in hover_cols if df[col].dtype == "object"]
    metric_cols = [col for col in hover_cols if col not in dimension_cols]

    layer_settings = {
        "lat_dim": lat,
        "long_dim": lon,
        "transparency": icon_opacity,
        "size": icon_size,
        "type": "point",
        "stroke": stroke_color,
        "stroke_width": stroke_width,
        "point_size_opts": point_size_opts,
        "hover_opts": {
            "dims": dimension_cols,
            "mets": metric_cols,
        },
        "tile_layer": tile_layer,
    }
    if label_column is not None:
        layer_settings["show_labels"] = label_column

    chart_settings = {
        "map_mode": "tile",
        "layer_settings": [layer_settings],
    }
    return handle_view(
        df,
        chart_mode="tilemap",
        chart=chart_settings,
        return_view=return_view,
        **kwargs,
    )
