from typing import List, Optional, Union

import pandas as pd
import structlog

from dx.formatters.main import handle_format
from dx.plotting.dex import _samples
from dx.settings import settings_context
from dx.types.dex_metadata import DEXMetadata, DEXView

logger = structlog.get_logger(__name__)


def dashboard(
    df: pd.DataFrame,
    views: List[Union[str, dict, list, DEXView]],
    **kwargs,
) -> Optional[DEXMetadata]:
    """
    Creates and renders a DEX dashboard from a list of views.

    Parameters
    ----------
    df: pd.DataFrame
        The dataframe to be rendered.
    views: List[Union[str, dict, list, DEXView]]
        A list of views to be created and rendered in the dashboard.
        By default, each item in the list will be treated as a row item.
        Each item in the list can be another nested list of views to
        determine column positioning within the dashboard view.
    """
    dex_metadata = DEXMetadata()
    multiview_order = []

    # generate and add views, assuming a matrix-like structure
    for row_num, views_row in enumerate(views):
        if not isinstance(views_row, list):
            views_row = [views_row]
        for col_num, view in enumerate(views_row):
            if isinstance(view, str):
                # direct dataframe-to-view
                view = view.lower()
                if view == "grid":
                    dex_view = DEXView.parse_obj({"chart_mode": view})
                else:
                    # TODO: remove this once all the chart functions are available
                    sample_chart_func = getattr(_samples, f"sample_{view}")
                    if sample_chart_func is None:
                        raise NotImplementedError(
                            f"No `sample_{view}` chart function available yet."
                        )
                    dex_view = sample_chart_func(df, return_view=True)
            elif isinstance(view, dict):
                # view dict
                dex_view = DEXView.parse_obj(view)
            elif isinstance(view, DEXView):
                dex_view = view
            else:
                raise ValueError(f"Invalid view type: {type(view)}")

            # make the views available for reference
            dex_dashboard_view = dex_view.copy(
                update={"is_default": False, "chartMode": dex_view.chart_mode}
            )
            # TODO: make DEXMetadata.add_view() support adding DEXView
            # instead of just dictionaries
            dex_dashboard_view_dict = dex_dashboard_view.dict(
                by_alias=True,
                exclude_none=True,
            )
            logger.debug(f"{dex_dashboard_view_dict=}")
            dex_metadata.views.append(dex_dashboard_view_dict)
            # define the view positioning
            multiview = {
                "column": col_num,
                "row": row_num,
                "id": str(dex_dashboard_view.id),
            }
            multiview_order.append(multiview)

    dashboard_view_metadata = {
        "views": multiview_order,
        "isDefault": True,
        "decoration": {
            "title": "🤔 dx dashboard",
        },
    }
    dashboard_view_metadata.update(kwargs)

    dex_dashboard_metadata = DEXView.parse_obj(dashboard_view_metadata)

    with settings_context(generate_dex_metadata=True):
        handle_format(
            df,
            extra_metadata={
                "dashboard": {
                    "multiViews": [
                        dex_dashboard_metadata.dict(by_alias=True),
                    ],
                },
                "views": dex_metadata.views,
            },
        )
