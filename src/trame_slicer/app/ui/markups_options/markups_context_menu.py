from dataclasses import dataclass
from typing import Any

from slicer import vtkMRMLMarkupsFiducialNode, vtkMRMLMarkupsNode
from trame.widgets.vuetify3 import VList
from trame_server.utils.typed_state import TypedState

from .fiducial_options_ui import FiducialMarkupOptionsUI


@dataclass
class MarkupsContextMenuState:
    selected_markups_id: str = ""

class MarkupsContextMenu(VList):
    def __init__(self):
        super().__init__(width="300px")
        self._typed_state = TypedState(self.state, MarkupsContextMenuState)
        self.markups_options_uis: dict[type[vtkMRMLMarkupsNode], Any] = {}

        self._register_ui(vtkMRMLMarkupsFiducialNode, FiducialMarkupOptionsUI)
 
    def is_selected_markup_type(self, markup_type: vtkMRMLMarkupsNode):
        return ("true", )
        name = str(markup_type)
        return (f"{self._typed_state.name.selected_markups_type} === {name}", )

    def _register_ui(self, markup_type: vtkMRMLMarkupsNode, markup_ui):
        ui_instance = markup_ui(v_if=self.is_selected_markup_type(markup_type))
        self.markups_options_uis[markup_type] = ui_instance