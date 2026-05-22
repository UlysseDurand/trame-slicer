from slicer import vtkMRMLMarkupsFiducialNode
from trame_server import Server
from trame_server.utils.typed_state import TypedState

from trame_slicer.core import SlicerApp

from ...ui import FiducialMarkupOptionsUI, MarkupsContextMenu
from .base_markups_option_logic import BaseMarkupOptionLogic


class FiducialOptionsLogic(BaseMarkupOptionLogic):
    def __init__(self, server: Server, slicer_app: SlicerApp, markups_context_menu_state: TypedState):
        super().__init__(server, slicer_app)
        self._markups_context_menu_state = markups_context_menu_state

    def set_options_ui(self, options_ui: FiducialMarkupOptionsUI):
        options_ui.delete_control_point.connect(self.delete_control_point)
        options_ui.select_control_point.connect(self.select_control_point)
        options_ui.unselect_control_point.connect(self.unselect_control_point)
    
    def set_ui(self, ui: MarkupsContextMenu):
        self.set_options_ui(ui.markups_options_uis[vtkMRMLMarkupsFiducialNode])
    
    def delete_control_point(self):
        markups_node_id = self._markups_context_menu_state.name.clicked_markups_node_id
        markups_node : vtkMRMLMarkupsFiducialNode = self._slicer_app.scene.GetNodeByID(markups_node_id)

        display_node = markups_node.GetDisplayNode()
        if display_node is None:
            return 
        active_index = display_node.GetActiveComponentIndex()
        if 0 <= active_index < markups_node.GetNumberOfControlPoints():
            markups_node.RemoveNthControlPoint(active_index)
    
    def select_control_point(self):
        markups_node_id = self._markups_context_menu_state.name.clicked_markups_node_id
        markups_node: vtkMRMLMarkupsFiducialNode = self._slicer_app.scene.GetNodeByID(markups_node_id)
        display_node = markups_node.GetDisplayNode()
        if display_node is None:
            return

        active_index = display_node.GetActiveComponentIndex()
        if 0 <= active_index < markups_node.GetNumberOfControlPoints():
            markups_node.SetNthControlPointSelected(active_index, True)
    
    def unselect_control_point(self):
        markups_node_id = self._markups_context_menu_state.name.clicked_markups_node_id
        markups_node: vtkMRMLMarkupsFiducialNode = self._slicer_app.scene.GetNodeByID(markups_node_id)
        display_node = markups_node.GetDisplayNode()
        if display_node is None:
            return

        active_index = display_node.GetActiveComponentIndex()
        if 0 <= active_index < markups_node.GetNumberOfControlPoints():
            markups_node.SetNthControlPointSelected(active_index, False) 