from trame.widgets import html
from trame.widgets.vuetify3 import (
    Template,
    VBtn,
    VCard,
    VTooltip,
)
from trame_server import Server

from trame_slicer.core import LayoutManager

from .control_button import ControlButton
from .download_scene_button import DownloadSceneButton
from .flex_container import FlexContainer
from .layout_button import LayoutButton
from .load_volume_ui import LoadVolumeUI
from .markups_button import MarkupsButton
from .markups_options import MarkupsContextMenu
from .mpr_interaction_button import MprInteractionButton
from .radial_markup_buttons import RadialMarkupsButton
from .segmentation import (
    SegmentEditorUI,
    SegmentEditorUndoRedoUI,
)
from .slab_button import SlabButton
from .viewer_layout import ViewerLayout
from .volume_property_ui import VolumePropertyUI


class MedicalViewerUI:
    def __init__(self, server: Server, layout_manager: LayoutManager):
        self.tool_registry = {}
        with ViewerLayout(server) as self.layout:
            self.layout.title.set_text("Medical Viewer")
            with self.layout.appbar, Template(v_slot_prepend=True):
                self.load_volume_items_buttons = LoadVolumeUI()
                self.download_scene_button = DownloadSceneButton()

            with self.layout.drawer:
                self._register_tool_ui(SegmentEditorUI)
                self._register_tool_ui(VolumePropertyUI)

            with self.layout.toolbar, FlexContainer(fill_height=True):
                self._create_tool_button(
                    icon="mdi-tune-variant",
                    name="Volume Properties",
                    tool_ui_type=VolumePropertyUI,
                )
                self.layout_button = LayoutButton()
                self.markups_button = MarkupsButton()
                self._create_tool_button(
                    icon="mdi-brush",
                    name="segmentation panel",
                    tool_ui_type=SegmentEditorUI,
                )
                self.slab_button = SlabButton()
                self.mpr_interaction_button = MprInteractionButton()

            with self.layout.undo_redo:
                self._register_undo_redo_ui(SegmentEditorUndoRedoUI, SegmentEditorUI)

            with self.layout.content:
                layout_manager.initialize_layout_grid(self.layout)
            
            with self.layout.tool_rad_menu:
                self.tool_registry[SegmentEditorUI].build_radial_menu_wheel_ui()
                self.radial_markups_buttons = RadialMarkupsButton(v_else="")

            with self.layout.tool_rad_menu.right_menu:
                self.tool_registry[SegmentEditorUI].build_radial_menu_side_menu_ui()
            
            with self.layout.tool_rad_menu.up_menu, VCard(style="width: 300px;"):
                self.tool_registry[SegmentEditorUI].build_segment_list_ui()
            
            with self.layout.tool_rad_menu.down_menu, VCard(style="width: 300px;"):
                self.tool_registry[SegmentEditorUI].build_masking_options_ui()

            with self.layout.tool_rad_menu.left_top:
                server.state.segment_menu_selected = False
                with (
                    VTooltip(text=("segment_menu_selected?'Markers':'Segments'",), location="start"),
                    html.Template(v_slot_activator="{ props }")
                ):
                    def toggle_segment_menu_selected():
                        server.state.segment_menu_selected = not(server.state.segment_menu_selected)
                        if not(server.state.segment_menu_selected):
                            server.state.tool_rad_menu_right_menu_open = False
                            server.state.tool_rad_menu_up_menu_open = False
                            server.state.tool_rad_menu_down_menu_open = False
                    VBtn(
                        icon=("segment_menu_selected ? 'mdi-circle-small' : 'mdi-brush'",),
                        v_bind="props",
                        color="#777d",
                        size=(40,),
                        click= toggle_segment_menu_selected,
                        active="segment_menu_selected",
                        variant="flat",
                    )

            with self.layout.tool_rad_menu.right_top:
                server.state.tool_rad_menu_right_menu_open = False
                with (
                    VTooltip(
                        text=("tool_rad_menu_right_menu_open ? 'Close segmentation tool options' : 'Open segmentation tool options'",), 
                        v_if="segment_menu_selected",
                        location="end"
                    ),
                    html.Template(v_slot_activator="{ props }")
                ):
                    def toggle_tool_rad_menu_right_menu_open():
                        server.state.tool_rad_menu_right_menu_open = not(server.state.tool_rad_menu_right_menu_open)
                    VBtn(
                        icon=("tool_rad_menu_right_menu_open?'mdi-chevron-left':'mdi-chevron-right'",), 
                        v_bind="props", 
                        color="#777d", 
                        size=(40,),
                        click=toggle_tool_rad_menu_right_menu_open,
                        active="tool_rad_menu_right_menu_open",
                        variant="flat",
                    )
                html.Div(v_else="")
            
            with self.layout.tool_rad_menu.top_left:
                server.state.tool_rad_menu_up_menu_open = False
                with (
                    VTooltip(
                        text=("tool_rad_menu_up_menu_open ? 'Close segments list' : 'Open segments list'",), 
                        v_if="segment_menu_selected",
                        location="top"
                    ),
                    html.Template(v_slot_activator="{ props }"),
                ):
                    def toggle_up_menu_open():
                        server.state.tool_rad_menu_up_menu_open = not(server.state.tool_rad_menu_up_menu_open)
                    VBtn(
                        icon=("tool_rad_menu_up_menu_open ? 'mdi-chevron-down' : 'mdi-chevron-up'",), 
                        v_bind="props", 
                        color="#777d", 
                        size=(40,),
                        click=toggle_up_menu_open,
                        active="tool_rad_menu_up_menu_open",
                        variant="flat",
                    )

            with self.layout.tool_rad_menu.bottom_left:
                server.state.tool_rad_menu_down_menu_open = False
                with (
                    VTooltip(
                        text=("tool_rad_menu_down_menu_open ? 'Close masking options' : 'Open masking options'",), 
                        v_if="segment_menu_selected",
                        location="bottom"
                    ),
                    html.Template(v_slot_activator="{ props }"),
                ):
                    def toggle_down_menu_open():
                        server.state.tool_rad_menu_down_menu_open = not(server.state.tool_rad_menu_down_menu_open)
                    VBtn(
                        icon="mdi-domino-mask", 
                        v_bind="props", 
                        color="#777d", 
                        size=(40,),
                        click=toggle_down_menu_open,
                        active="tool_rad_menu_down_menu_open",
                        variant="flat",
                    )

            with (
                self.layout.tool_rad_menu.bottom_right,
                VTooltip(text="Undo", v_if="segment_menu_selected", location="bottom"),
                html.Template(v_slot_activator="{ props }"),
            ):
                VBtn(
                    icon="mdi-undo", 
                    v_bind="props", 
                    color="#777d", 
                    size=(40,),
                    click=self.tool_registry[SegmentEditorUI].undo_clicked,
                    variant="flat",
                )

            with (
                self.layout.tool_rad_menu.right_bottom,
                VTooltip(text="Redo", v_if="segment_menu_selected", location="end"),
                html.Template(v_slot_activator="{ props }"),
            ):
                VBtn(
                    icon="mdi-redo", 
                    v_bind="props", 
                    color="#777d", 
                    size=(40,),
                    click=self.tool_registry[SegmentEditorUI].redo_clicked,
                    variant="flat",
                )
            
            server.state.markup_options_rad_menu_right_menu_open = True
            with self.layout.markup_options_rad_menu.right_menu:
                self.markups_button.markups_context_menu = MarkupsContextMenu()
            with self.layout.markup_options_rad_menu.top_right:
                html.Div()
            with self.layout.markup_options_rad_menu.right_top:
                html.Div()
            with self.layout.markup_options_rad_menu.central:
                html.Div()


    @property
    def data(self):
        return self.layout.typed_state.data

    @property
    def name(self):
        return self.layout.typed_state.name

    def _is_tool_active(self, tool_ui_type: type):
        return f"{self.name.active_tool} === '{tool_ui_type.__name__}'"

    def _is_tool_drawer_visible(self, tool_ui_type: type):
        return f"{self._is_tool_active(tool_ui_type)} && {self.name.is_drawer_visible}"

    def _register_tool_ui(self, tool_ui_type: type):
        tool_instance = tool_ui_type(v_if=(self._is_tool_active(tool_ui_type),))
        self.tool_registry[tool_ui_type] = tool_instance

    def _register_undo_redo_ui(self, undo_redo_ui_type: type, tool_ui_type: type):
        undo_redo_ui_type(
            editor_ui=self.tool_registry[tool_ui_type],
            v_if=(self._is_tool_active(tool_ui_type),),
        )

    def _create_tool_button(self, name: str, icon: str | tuple, tool_ui_type: type):
        async def change_drawer_ui():
            is_drawer_visible = not self.data.is_drawer_visible or self.data.active_tool != tool_ui_type.__name__
            self.data.is_drawer_visible = is_drawer_visible
            self.data.active_tool = tool_ui_type.__name__ if is_drawer_visible else None

        ControlButton(
            icon=icon,
            name="{{ " + f"{self._is_tool_drawer_visible(tool_ui_type)} ? 'Close {name}' : 'Open {name}'" + " }}",
            click=change_drawer_ui,
            active=(self._is_tool_active(tool_ui_type),),
        )
