from collections.abc import Callable

from trame.widgets.radial_menu import RadItem
from trame.widgets.vuetify3 import VBtn


class RadItemButton(RadItem):

    def __init__(
        self, 
        name: str, 
        icon: str | tuple, 
        click: Callable | str | None = None, 
        **kwargs,
    ) -> None:
        super().__init__(tooltipLabel=name, **kwargs)

        with self:
            VBtn(
                icon=icon,
                click=click,
                v_bind="props",
                color="#777d",
                variant="flat",
            )