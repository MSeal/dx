import pandas as pd
import structlog
from pydantic import parse_obj_as

from dx.formatters.main import handle_format
from dx.types.charts._base import chart_view_ref

logger = structlog.get_logger(__name__)


def handle_view(
    df: pd.DataFrame,
    chart: dict,
    chart_mode: str,
    return_view: bool = False,
    **kwargs,
):
    """
    Converts a chart dictionary to a DEXChartView-inherited object
    and either passes it to be handled by the display formatter,
    or returns the view.
    """
    logger.info(f"{chart=}")

    view = parse_obj_as(
        chart_view_ref(),
        {
            "chart_mode": chart_mode,
            "chart": chart,
            **kwargs,
        },
    )
    view_metadata = view.dict(
        exclude_unset=True,
        exclude_none=True,
        by_alias=True,
    )
    logger.info(f"{view_metadata=}")

    if return_view:
        return view_metadata
    handle_format(df, extra_metadata=view_metadata)
