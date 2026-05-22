from dataclasses import dataclass

from trame_server import Server
from trame_server.utils.typed_state import TypedState

from trame_slicer.app.logic.markups_options.base_markups_option_logic import (
    BaseMarkupOptionLogic,
)
from trame_slicer.core import SlicerApp

from ...ui import MarkupsContextMenu
from .fiducial_options_logic import FiducialOptionsLogic


@dataclass
class MarkupsContextMenuLogicState:
    clicked_markups_node_id: str = ""

class MarkupsContextMenuLogic:
    def __init__(self, server: Server, slicer_app: SlicerApp):
        self._server = server
        self._typed_state = TypedState(server.state, MarkupsContextMenuLogicState)
        self.markups_option_logics: list[BaseMarkupOptionLogic] = [
            FiducialOptionsLogic
        ]
        self._markups_option_logics = [Logic(server, slicer_app, self._typed_state) for Logic in self.markups_option_logics]
    
    def set_ui(self, ui: MarkupsContextMenu):
        for logic in self._markups_option_logics:
            logic.set_ui(ui)

    def set_clicked_node_id(self, id: str):
        self._typed_state.name.clicked_markups_node_id = id