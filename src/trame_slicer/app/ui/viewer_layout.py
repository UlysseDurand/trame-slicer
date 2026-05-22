from dataclasses import dataclass

from trame.ui.vuetify3 import VAppLayout
from trame.widgets import html
from trame.widgets.radial_menu import RadMenu
from trame.widgets.vuetify3 import (
    VAppBar,
    VBtn,
    VDivider,
    VFooter,
    VIcon,
    VMain,
    VNavigationDrawer,
    VProgressCircular,
    VSpacer,
    VToolbarTitle,
)
from trame_server import Server
from trame_server.utils.typed_state import TypedState

from .flex_container import FlexContainer


@dataclass
class ViewerLayoutState:
    is_drawer_visible: bool = False
    active_tool: str | None = None
    is_volume_loaded: bool = False


class ViewerLayout(VAppLayout):
    def __init__(
        self,
        server: Server,
        template_name="main",
        title: str = "Trame Slicer",
        theme: str = "dark",
        is_drawer_visible: bool = False,
    ):
        super().__init__(server, template_name=template_name)
        self.typed_state = TypedState(self.state, ViewerLayoutState)
        self.typed_state.data.is_drawer_visible = is_drawer_visible

        self.root.theme = theme

        with self:
            with VAppBar() as self.appbar:
                self.title = VToolbarTitle(title, style="user-select: none;")

            with VFooter(app=True, classes="my-0 py-0", border=True) as self.footer:
                VProgressCircular(
                    indeterminate=("!!trame__busy",),
                    color="#04a94d",
                    size=16,
                    width=3,
                    classes="ml-n3 mr-1",
                )
                self.footer.add_child(
                    '<a href="https://kitware.github.io/trame/" '
                    'class="text-grey-lighten-1 text-caption text-decoration-none" '
                    'target="_blank">Powered by trame</a>'
                )
                VSpacer()
                reload = self.server.controller.on_server_reload
                if reload.exists():
                    with VBtn(
                        size="x-small",
                        density="compact",
                        icon=True,
                        # border=True,
                        elevation=0,
                        click=self.on_server_reload,
                        classes="mx-2",
                    ):
                        VIcon("mdi-autorenew", size="small")

                self.footer.add_child(
                    '<a href="https://www.kitware.com/" '
                    'class="text-grey-lighten-1 text-caption text-decoration-none" '
                    'target="_blank">© 2025 Kitware Inc.</a>'
                )

            with VMain():
                self.content = FlexContainer(row=True, fill_height=True)

            def close_tool_rad_menu():
                server.state.tool_rad_menu_open = False
            def open_tool_rad_menu_at_mouse_pos():
                server.js_call(ref="toolRadMenu", method="openAtCursor")
            server.controller.close_tool_rad_menu = close_tool_rad_menu
            server.controller.open_tool_rad_menu_at_mouse_pos = open_tool_rad_menu_at_mouse_pos

            with RadMenu(
                ref="toolRadMenu",
                v_model_open=("tool_rad_menu_open", False), 
                v_model_rightmenuopen=("tool_rad_menu_right_menu_open",), 
                v_model_upmenuopen=("tool_rad_menu_up_menu_open",), 
                v_model_downmenuopen=("tool_rad_menu_down_menu_open",), 
                open_at_right_click_pos=False,
                color="#777d"
            ) as self.tool_rad_menu:
                self.tool_rad_menu.right_menu = html.Template(v_slot_right_menu="")
                self.tool_rad_menu.up_menu = html.Template(v_slot_up_menu="")
                self.tool_rad_menu.down_menu = html.Template(v_slot_down_menu="")
                self.tool_rad_menu.bottom_right = html.Template(v_slot_bottom_right="")
                self.tool_rad_menu.right_bottom = html.Template(v_slot_right_bottom="")
                self.tool_rad_menu.right_top = html.Template(v_slot_right_top="")
                self.tool_rad_menu.top_right = html.Template(v_slot_top_right="")
                self.tool_rad_menu.top_left = html.Template(v_slot_top_left="")
                self.tool_rad_menu.left_top = html.Template(v_slot_left_top="")
                self.tool_rad_menu.left_bottom = html.Template(v_slot_left_bottom="")
                self.tool_rad_menu.bottom_left = html.Template(v_slot_bottom_left="")
            
            def close_markup_options_rad_menu():
                server.state.markup_options_rad_menu_open = False
            def open_marker_options_rad_menu_at_mouse_pos():
                server.js_call(ref="markupOptionsRadMenu", method="openAtCursor")
            server.controller.close_markup_options_rad_menu = close_markup_options_rad_menu
            server.controller.open_markup_options_rad_menu_at_mouse_pos = open_marker_options_rad_menu_at_mouse_pos

            with RadMenu(
                ref="markupOptionsRadMenu",
                v_model_open=("markup_options_rad_menu_open", False), 
                v_model_rightmenuopen=("markup_options_rad_menu_right_menu_open", True),
                open_at_right_click_pos=False,
                color="#777d"
            ) as self.markup_options_rad_menu:
                self.markup_options_rad_menu.central = html.Template(v_slot_central="")
                self.markup_options_rad_menu.right_menu = html.Template(v_slot_right_menu="")
                self.markup_options_rad_menu.bottom_right = html.Template(v_slot_bottom_right="")
                self.markup_options_rad_menu.right_bottom = html.Template(v_slot_right_bottom="")
                self.markup_options_rad_menu.right_top = html.Template(v_slot_right_top="")
                self.markup_options_rad_menu.top_right = html.Template(v_slot_top_right="")
                self.markup_options_rad_menu.top_left = html.Template(v_slot_top_left="")
                self.markup_options_rad_menu.left_top = html.Template(v_slot_left_top="")
                self.markup_options_rad_menu.left_bottom = html.Template(v_slot_left_bottom="")
                self.markup_options_rad_menu.bottom_left = html.Template(v_slot_bottom_left="")

            self.drawer = VNavigationDrawer(
                disable_resize_watcher=True,
                disable_route_watcher=True,
                permanent=True,
                location="left",
                v_model=(self.typed_state.name.is_drawer_visible, is_drawer_visible),
                width=350,
            )


            with (
                VNavigationDrawer(
                    disable_resize_watcher=True,
                    disable_route_watcher=True,
                    permanent=True,
                    width=40,
                    location="left",
                ),
                FlexContainer(fill_height=True),
            ):
                self.toolbar = FlexContainer(classes="py-2", align="center")
                VDivider()
                VSpacer()
                VDivider()
                self.undo_redo = FlexContainer(classes="py-2", align="center")
