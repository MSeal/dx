import enum
import uuid
from typing import Optional

from IPython.display import HTML, display
from pydantic import BaseModel


class CalloutLevel(enum.Enum):
    primary = "primary"
    secondary = "secondary"
    info = "info"
    warning = "warning"
    danger = "danger"


class CalloutIcon(enum.Enum):
    info = "info"
    warning = "warning"


class Callout(BaseModel):
    icon: Optional[CalloutIcon] = None
    level: CalloutLevel = CalloutLevel.info
    message: str
    use_header: bool = True

    @property
    def html(self):
        callout_classes = [
            "bp3-callout",
            f"bp3-intent-{self.level.value}",
        ]
        if self.icon is not None:
            callout_classes.append(f"bp3-icon-{self.icon.value}-sign")
        callout_class_str = " ".join(callout_classes)

        if self.use_header:
            heading_html = f"<h6 class='bp3-heading'>{self.level.value.title()}</h6>"
            return f"<div class='{callout_class_str}'>{heading_html}{self.message}</div>"

        return f"<div class='{callout_classes}'>{self.message}</div>"


def display_callout(
    message: str,
    level: CalloutLevel = CalloutLevel.info,
    header: bool = True,
    icon: Optional[CalloutIcon] = None,
    display_id: str = None,
) -> None:
    callout = Callout(
        message=message,
        level=level,
        use_header=header,
        icon=icon,
    )
    display_id = display_id or str(uuid.uuid4())
    display(HTML(callout.html), display_id=display_id)
