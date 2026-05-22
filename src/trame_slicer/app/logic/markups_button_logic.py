import vtk
from slicer import (
    vtkMRMLDisplayNode,
    vtkMRMLMarkupsNode,
    vtkMRMLScene,
)
from trame_server import Server
from vtkmodules.vtkCommonCore import VTK_OBJECT

from trame_slicer.core import SlicerApp

from ..ui import MarkupsButton
from .base_logic import BaseLogic
from .markups_options.markups_context_menu_logic import MarkupsContextMenuLogic


class MarkupsButtonLogic(BaseLogic):
    def __init__(self, server: Server, slicer_app: SlicerApp):
        super().__init__(server, slicer_app, None)
        self._markup_nodes = []
        self._slicer_app.scene.AddObserver(vtkMRMLScene.NodeAddedEvent, self._on_node_added)
        self._markups_context_menu_logic = MarkupsContextMenuLogic(server, slicer_app)
    
    @vtk.calldata_type(VTK_OBJECT)
    def _on_node_added(self, _scene, _event_id, node):
        if isinstance(node, vtkMRMLDisplayNode):
            node.AddObserver(vtkMRMLDisplayNode.MenuEvent, self._on_menu_event)

    def _on_menu_event(self, caller, _event):
        markups_node = caller.GetDisplayableNode()
        if markups_node is None:
            return
        self._markups_context_menu_logic.set_clicked_node_id(markups_node.GetID())
        self._server.controller.open_markup_options_rad_menu_at_mouse_pos()

    def set_ui(self, ui: MarkupsButton):
        ui.place_node_type.connect(self.on_place_node_type)
        ui.clear_clicked.connect(self.on_clear_clicked)
        self._markups_context_menu_logic.set_ui(ui.markups_context_menu)

    def on_clear_clicked(self) -> None:
        for node in self._markup_nodes:
            self._slicer_app.scene.RemoveNode(node)

    def _create_node(self, node_type: str) -> vtkMRMLMarkupsNode:
        node = self._slicer_app.scene.AddNewNodeByClass(node_type)
        if node:
            self._markup_nodes.append(node)
        return node

    def on_place_node_type(self, node_type: str, is_persistent: bool) -> None:
        node = self._create_node(node_type)
        if node is not None:
            self._slicer_app.markups_logic.place_node(node, is_persistent)
