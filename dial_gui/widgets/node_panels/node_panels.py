# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:
import random
from typing import TYPE_CHECKING, List

import dependency_injector.providers as providers
from PySide2.QtCore import QEvent, QObject, Qt, Signal
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QDialog, QDockWidget, QMainWindow, QVBoxLayout, QWidget

if TYPE_CHECKING:
    from dial_gui.node_editor import GraphicsNode


class NodePanel(QDockWidget):
    def __init__(self, graphics_node: "GraphicsNode", parent: "QWidget" = None):
        super().__init__(graphics_node.title, parent)

        self.__graphics_node = graphics_node

        self.__proxy_widget = self.__graphics_node._proxy_widget

        self.__inner_widget = self.__proxy_widget.widget()
        self.__last_size = self.__inner_widget.size()

    @property
    def graphics_node(self) -> "GraphicsNode":
        return self.__graphics_node

    def event(self, event: "QEvent"):
        if event.type() == QEvent.Show:
            self.__enable()
            return True

        if event.type() == QEvent.Hide:
            self.__disable()
            return True

        return super().event(event)

    def __enable(self):
        self.__last_size = self.__inner_widget.size()

        self.__graphics_node.set_inner_widget(QWidget())

        self.setWidget(self.__inner_widget)

    def __disable(self):
        self.setWidget(None)
        self.__inner_widget.setParent(None)

        dialog = QDialog()

        layout = QVBoxLayout()
        layout.addWidget(self.__inner_widget)
        dialog.setLayout(layout)

        dialog.show()

        self.__inner_widget.setParent(None)

        self.__inner_widget.resize(self.__last_size)
        self.__graphics_node.set_inner_widget(self.__inner_widget)

        dialog.close()


class NodesWindow(QMainWindow):
    def __init__(
        self,
        node_panel_factory: "providers.Factory",
        name="NodesWindow",
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        self.name = name

        self.__node_panel_factory = node_panel_factory
        self.__node_panels: List["ViewportNodeBlock"] = []

        self.color_identifier = QColor.fromHsvF(random.random(), 0.65, 0.6)

        self.setCentralWidget(QWidget())

    @property
    def node_panels(self) -> List["NodePanel"]:
        return self.__node_panels

    def add_graphics_node(self, graphics_node: "GraphicsNode"):
        viewport_node_block = self.__node_panel_factory(graphics_node, parent=self)
        self.__node_panels.append(viewport_node_block)
        graphics_node.parent_node_windows.append(self)
        print(graphics_node.parent_node_windows)

        if len(self.__node_panels) % 2:
            self.addDockWidget(Qt.RightDockWidgetArea, viewport_node_block)
        else:
            self.addDockWidget(Qt.LeftDockWidgetArea, viewport_node_block)

    def clear(self):
        for node_panel in self.__node_panels:
            try:
                node_panel.graphics_node.parent_node_windows.remove(self)
            except ValueError:
                pass


class NodesWindowsManager(QObject):
    new_nodes_window_created = Signal(NodesWindow)
    nodes_window_added = Signal(NodesWindow)
    nodes_window_removed = Signal(NodesWindow)

    def __init__(
        self, nodes_windows_factory: "providers.Factory", parent: "QObject" = None
    ):
        super().__init__(parent)

        self.__nodes_windows_factory = nodes_windows_factory
        self.__nodes_windows = []

    @property
    def nodes_windows(self):
        return self.__node_windows

    def new_nodes_window(self) -> "NodesWindow":
        nodes_window = self._new_nodes_impl()

        return self.add_nodes_window(nodes_window)

    def add_nodes_window(self, nodes_window: "NodesWindow") -> "NodesWindow":
        return self._add_nodes_window_impl(nodes_window)

    def remove_nodes_window(self, nodes_window: "NodesWindow"):
        self._remove_nodes_window_impl(nodes_window)

    def _new_nodes_impl(self) -> "NodesWindow":
        nodes_window = self.__nodes_windows_factory(
            name=f"Nodes Window {len(self.__nodes_windows) + 1}"
        )
        self.new_nodes_window_created.emit(nodes_window)
        return nodes_window

    def _add_nodes_window_impl(self, nodes_window: "NodesWindow"):
        self.__nodes_windows.append(nodes_window)
        self.nodes_window_added.emit(nodes_window)
        return nodes_window

    def _remove_nodes_window_impl(self, nodes_window: "NodesWindow"):
        try:
            self.__nodes_windows.remove(nodes_window)
            self.nodes_window_removed.emit(nodes_window)
            nodes_window.clear()

        except ValueError:
            pass


NodePanelFactory = providers.Factory(NodePanel)
NodesWindowFactory = providers.Factory(NodesWindow, NodePanelFactory.delegate())

NodesWindowsManagerSingleton = providers.Singleton(
    NodesWindowsManager, nodes_windows_factory=NodesWindowFactory.delegate()
)