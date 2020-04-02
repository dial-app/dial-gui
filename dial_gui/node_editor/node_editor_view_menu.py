# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QAction, QMenu

from .graphics_node import GraphicsNode

if TYPE_CHECKING:
    from .graphics_scene import GraphicsScene
    from dial_gui.widgets.node_panels import NodesWindowsManager
    from PySide2.QtWidgets import QWidget
    from dial_gui.widgets.node_panels import NodesWindow


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
            self.__add_selected_nodes_to_new_window
        )

        self._add_each_node_to_new_window_act = QAction(
            "Add each node to a new window", self
        )
        self._add_each_node_to_new_window_act.triggered.connect(
            self.__add_each_selected_node_to_new_window
        )

        self._add_nodes_to_existing_window_menu = QMenu(
            "Add nodes to existing window...", self
        )

        if len(self.__nodes_windows_manager.nodes_windows) == 0:
            self._add_nodes_to_existing_window_menu.setEnabled(False)

        for window in self.__nodes_windows_manager.nodes_windows:
            action = self._add_nodes_to_existing_window_menu.addAction(window.name)
            action.triggered.connect(
                lambda _=None, window=window: (
                    self.__add_selected_nodes_to_existing_window(window)
                )
            )

        self.addAction(self._remove_elements_act)
        self.addSeparator()
        self.addAction(self._add_nodes_to_new_window_act)
        self.addAction(self._add_each_node_to_new_window_act)
        self.addMenu(self._add_nodes_to_existing_window_menu)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:  # Ignore right clicks
            return

        super().mouseReleaseEvent(event)

    def __remove_selected_elements(self):
        """Remove the selected elements from the scene."""
        for selected_item in self.__graphics_scene.selectedItems():
            self.__graphics_scene.removeItem(selected_item)

        self.__graphics_scene.update()

    def __add_selected_nodes_to_new_window(self):
        """Add the selected nodes from a new NodesWindow object."""
        nodes_window = self.__nodes_windows_manager.new_nodes_window()
        self.__add_nodes_to_window(self.__graphics_scene.selectedItems(), nodes_window)

    def __add_selected_nodes_to_existing_window(self, window: "NodesWindow"):
        """Add the selected nodes to a currently existing NodesWindow object."""
        self.__add_nodes_to_window(self.__graphics_scene.selectedItems(), window)

    def __add_each_selected_node_to_new_window(self):
        """For each selected node, add it to a new window."""
        for item in self.__graphics_scene.selectedItems():
            if isinstance(item, GraphicsNode):
                nodes_window = self.__nodes_windows_manager.new_nodes_window(
                    name=item.title
                )
                self.__add_nodes_to_window([item], nodes_window)

    def __add_nodes_to_window(self, graphics_nodes, window):
        """Add the nodes to the passed window."""
        for graphics_node in graphics_nodes:
            if isinstance(graphics_node, GraphicsNode):
                window.add_graphics_node(graphics_node)


NodeEditorViewMenuFactory = providers.Factory(NodeEditorViewMenu)
