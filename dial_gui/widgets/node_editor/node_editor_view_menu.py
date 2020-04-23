# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QAction, QMenu

from dial_gui.node_editor import GraphicsNode

if TYPE_CHECKING:
    from .graphics_scene import GraphicsScene
    from dial_gui.node_editor.nodes_windows import NodesWindowsGroup, NodesWindow
    from PySide2.QtWidgets import QWidget


class NodeEditorViewMenu(QMenu):
    """The NodeEditorViewMenu class provides a menu for the options avaliable on the
    menu (Like duplicating nodes, adding them to windows, etc).
    """

    remove_nodes = Signal()
    duplicate_nodes = Signal()

    def __init__(
        self,
        graphics_scene: "GraphicsScene",
        nodes_windows_manager: "NodesWindowsGroup",
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        # Components
        self.__graphics_scene = graphics_scene
        self.__nodes_windows_manager = nodes_windows_manager

        # Actions
        self._remove_nodes_act = QAction("Remove nodes", self)
        self._remove_nodes_act.triggered.connect(lambda: self.remove_nodes.emit())

        self._duplicate_nodes_act = QAction("Duplicate nodes", self)
        self._duplicate_nodes_act.triggered.connect(lambda: self.duplicate_nodes.emit())

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

        # Add an entry for each opened window
        for window in self.__nodes_windows_manager.nodes_windows:
            action = self._add_nodes_to_existing_window_menu.addAction(window.name)
            action.triggered.connect(
                lambda _=None, window=window: (
                    self.__add_selected_nodes_to_existing_window(window)
                )
            )

        self.addAction(self._remove_nodes_act)
        self.addAction(self._duplicate_nodes_act)
        self.addSeparator()
        self.addAction(self._add_nodes_to_new_window_act)
        self.addAction(self._add_each_node_to_new_window_act)
        self.addMenu(self._add_nodes_to_existing_window_menu)

    def mouseReleaseEvent(self, event):
        """Ignore right clicks on the QMenu (Avoids unintentional clicks)"""
        if event.button() == Qt.RightButton:  # Ignore right clicks
            return

        super().mouseReleaseEvent(event)

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
