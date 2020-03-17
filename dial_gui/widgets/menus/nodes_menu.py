# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers

from typing import TYPE_CHECKING

from PySide2.QtWidgets import QAction, QMenu
from dial_core.node_editor import NodeRegistrySingleton

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget
    from dial_core.node_editor import NodeRegistry, Node
    from dial_gui.node_editor import GraphicsScene, NodeEditorView


class NodesMenu(QMenu):
    def __init__(
        self,
        node_registry: "NodeRegistry",
        graphics_scene: "GraphicsScene",
        node_editor_view: "NodeEditorView",
        parent: "QWidget" = None,
    ):
        super().__init__("&Nodes", parent)

        self.__graphics_scene = graphics_scene
        self.__node_editor_view = node_editor_view

        for node_name, factory in node_registry.nodes.items():
            action = QAction(node_name, self)

            action.triggered.connect(
                lambda _=False, create_node=factory: self.__add_node_to_scene(
                    create_node()
                )
            )

            self.addAction(action)

    def __add_node_to_scene(self, node: "Node"):
        graphics_node = self.__graphics_scene.add_node_to_graphics(node)

        global_pos = self.__node_editor_view.mapFromGlobal(self.pos())
        graphics_node.setPos(self.__node_editor_view.mapToScene(global_pos))

NodesMenuFactory = providers.Factory(NodesMenu, node_registry=NodeRegistrySingleton)
