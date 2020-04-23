# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from PySide2.QtWidgets import QVBoxLayout, QWidget

from dial_gui.node_editor import GraphicsSceneFactory
from .node_editor_view import NodeEditorViewFactory

if TYPE_CHECKING:
    from .node_editor_view import NodeEditorView
    from dial_gui.node_editor import GraphicsScene


class NodeEditorWindow(QWidget):
    def __init__(
        self,
        node_editor_view: "NodeEditorView",
        graphics_scene: "GraphicsScene",
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        self.__node_editor_view = node_editor_view
        self.__node_editor_view.setParent(self)

        self.__graphics_scene = graphics_scene
        self.__node_editor_view.setScene(self.__graphics_scene)

        self.__main_layout = QVBoxLayout()
        self.__main_layout.addWidget(self.__node_editor_view)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__main_layout)

    def change_view(self, new_node_editor_view: "NodeEditorView"):
        self.__node_editor_view = new_node_editor_view
        self.__node_editor_view.setScene(self.__graphics_scene)

    def change_graphics_scene(self, new_graphics_scene: "GraphicsScene"):
        self.__graphics_scene = new_graphics_scene
        self.__node_editor_view.setScene(self.__graphics_scene)


NodeEditorWindowFactory = providers.Factory(
    NodeEditorWindow,
    node_editor_view=NodeEditorViewFactory,
    graphics_scene=GraphicsSceneFactory,
)
