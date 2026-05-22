from abc import ABC, abstractmethod

from trame_server import Server

from trame_slicer.core import SlicerApp

# from .markups_context_menu_logic import MarkupsContextMenu


class BaseMarkupOptionLogic(ABC):
    def __init__(self, server: Server, slicer_app: SlicerApp):
        self._server = server
        self._slicer_app = slicer_app

    @abstractmethod
    def set_ui(self, ui):
        pass
