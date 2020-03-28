# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_gui.widgets.node_panels import NodesWindowsManagerSingleton
from PySide2.QtWidgets import QAction, QMenu

from .graphics_node import GraphicsNode

if TYPE_CHECKING:
    from .graphics_scene import GraphicsScene
    from dial_gui.widgets.node_panels import NodesWindowsManager
    from PySide2.QtWidgets import QWidget


class NodeEditorViewMenu(QMenu):
    def __init__(
        self,
        graphics_scene: "GraphicsScene",
        nodes_windows_manager: "NodesWindowsManager",
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        self.__graphics_scene = graphics_scene
        self.__nodes_windows_manager = nodes_windows_manager

        self._remove_elements_act = QAction("Remove nodes", self)
        self._remove_elements_act.triggered.connect(self.__remove_selected_elements)

        self._add_nodes_to_new_window_act = QAction("Add nodes to new window", self)
        self._add_nodes_to_new_window_act.triggered.connect(
            self.__add_nodes_to_new_window
        )

        self._add_nodes_to_existing_viewport_menu = QMenu(
            "Add nodes to existing window...", self
        )
        # for viewport in self.node_editor_view.scene().selected_item():
        #     action = self._add_nodes_to_existing_viewport_menu.addAction("asdf")
        #     action.triggered.connect(
        #         lambda _=None, viewport=viewport: self.__add_nodes_to_existing_viewport(
        #             viewport
        #         )
        #     )

        self.addAction(self._remove_elements_act)
        self.addSeparator()
        self.addAction(self._add_nodes_to_new_window_act)
        self.addMenu(self._add_nodes_to_existing_viewport_menu)

    def __remove_selected_elements(self):
        for selected_item in self.__graphics_scene.selectedItems():
            self.__graphics_scene.removeItem(selected_item)

        self.__graphics_scene.update()

    def __add_nodes_to_new_window(self):
        nodes_window = self.__nodes_windows_manager.new_nodes_window()

        for selected_item in self.__graphics_scene.selectedItems():
            if isinstance(selected_item, GraphicsNode):
                nodes_window.add_graphics_node(selected_item)

    def __add_nodes_to_existing_viewport(self, viewport):
        print("ASDf")


NodeEditorViewMenuFactory = providers.Factory(
    NodeEditorViewMenu, nodes_windows_manager=NodesWindowsManagerSingleton
)
