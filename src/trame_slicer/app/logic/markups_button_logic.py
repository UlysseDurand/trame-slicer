import vtk
from slicer import (
    vtkMRMLDisplayNode,
    vtkMRMLMarkupsAngleNode,
    vtkMRMLMarkupsClosedCurveNode,
    vtkMRMLMarkupsCurveNode,
    vtkMRMLMarkupsFiducialNode,
    vtkMRMLMarkupsLineNode,
    vtkMRMLMarkupsNode,
    vtkMRMLMarkupsPlaneNode,
    vtkMRMLMarkupsROINode,
    vtkMRMLScene,
)
from trame_server import Server
from vtkmodules.vtkCommonCore import VTK_OBJECT

from trame_slicer.core import SlicerApp

from ..ui import MarkupsButton
from .base_logic import BaseLogic


class MarkupsButtonLogic(BaseLogic):
    def __init__(self, server: Server, slicer_app: SlicerApp):
        super().__init__(server, slicer_app, None)
        self._markup_nodes = []
        self._slicer_app.scene.AddObserver(vtkMRMLScene.NodeAddedEvent, self._on_node_added)
    
    @vtk.calldata_type(VTK_OBJECT)
    def _on_node_added(self, _scene, _event_id, node):
        if isinstance(node, vtkMRMLDisplayNode):

            node.AddObserver(vtkMRMLDisplayNode.MenuEvent, self._on_menu_event)

    def _on_menu_event(self, caller, _event):
        markups_node = caller.GetDisplayableNode()
        if isinstance(markups_node, vtkMRMLMarkupsFiducialNode):
            print("This is a Fiducial")
        elif isinstance(markups_node, vtkMRMLMarkupsLineNode):
            print("This is a MarkupsLine")
        elif isinstance(markups_node, vtkMRMLMarkupsAngleNode):
            print("This is a Angle")
        elif isinstance(markups_node, vtkMRMLMarkupsClosedCurveNode):
            print("This is a ClosedCurve")
        elif isinstance(markups_node, vtkMRMLMarkupsCurveNode):
            print("This is a Curve")
        elif isinstance(markups_node, vtkMRMLMarkupsPlaneNode):
            print("This is a Plane")
        elif isinstance(markups_node, vtkMRMLMarkupsROINode):
            print("This is a ROI")
        else:
            print("What is this ?")


    def set_ui(self, ui: MarkupsButton):
        ui.place_node_type.connect(self.on_place_node_type)
        ui.clear_clicked.connect(self.on_clear_clicked)

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
