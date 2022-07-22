import enum

from IPython.display import HTML, display
from pydantic import BaseModel


class CalloutLevel(enum.Enum):
    primary = "primary"
    secondary = "secondary"
    info = "info"
    warning = "warning"
    danger = "danger"


class Callout(BaseModel):
    message: str
    level: CalloutLevel = CalloutLevel.info

    @property
    def html(self):
        heading_html = f"<h6 class='bp3-heading'>{self.level.value.title()}</h6>"
        callout_classes = " ".join(
            [
                "bp3-callout",
                f"bp3-intent-{self.level.value}",
            ]
        )
        return f"<div class='{callout_classes}'>{heading_html}{self.message}</div>"


def display_callout(
    message: str,
    level: CalloutLevel = CalloutLevel.info,
) -> None:
    callout = Callout(message=message, level=level)
    display(HTML(callout.html))
