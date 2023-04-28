from typing import List, Optional

import pandas as pd
import structlog
from pydantic import parse_obj_as

from dx.formatters.main import handle_format
from dx.settings import settings_context
from dx.types.charts import dex_charts
from dx.types.charts._base import DEXChartBase
from dx.types.dex_metadata import DEXView

logger = structlog.get_logger(__name__)


def handle_view(
    df: pd.DataFrame,
    chart_mode: str,
    chart: Optional[dict] = None,
    return_view: bool = False,
    **kwargs,
) -> Optional[DEXView]:
    """
    Primary function that takes a DataFrame and chart information to coerce it into a DEXView after
    parsing the chart information into a DEXChartView object. Once modeled, it will either be
    handled by the display formatter, or will return the view.
    """
    logger.debug(f"{chart=}")

    view_params = {
        "chart_mode": chart_mode,
        "chart": DEXChartBase.parse_obj(chart or {}),
        "decoration": {"title": chart_mode.title()},
    }
    view_params.update(kwargs)

    view = parse_obj_as(dex_charts, view_params)

    if view.chart.summary_type is not None:
        # show "Summary (Violin)" instead of just "Summary"
        view.decoration.title = f"{view.decoration.title} ({view.chart.summary_type})"

    if return_view:
        return view

    view_metadata = view.dict(
        exclude_unset=True,
        exclude_none=True,
        by_alias=True,
    )
    logger.debug(f"{view_metadata=}")
    with settings_context(generate_dex_metadata=True):
        handle_format(df, extra_metadata=view_metadata)


def raise_for_missing_columns(columns: List[str], existing_columns: pd.Index) -> None:
    """
    Checks if a column exists in a dataframe or is "index".
    If both fail, this raises a ValueError.
    """
    if isinstance(columns, str):
        columns = [columns]

    for column in columns:
        if str(column) == "index":
            return
        if column in existing_columns:
            return
        raise ValueError(f"Column `{column}` not found in DataFrame")
