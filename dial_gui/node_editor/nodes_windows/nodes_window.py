# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import random

import dependency_injector.providers as providers
from dial_gui.node_editor import GraphicsNode
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QMainWindow, QSizePolicy, QWidget

from .node_panel import NodePanel, NodePanelFactory


class NodesWindow(QMainWindow):
    """The NodesWindow class provides a container for several GraphicsNode objects, that
    are stored and displayed by using NodePanels.

    The NodesWindow class mimicks the Qt Dock Widget system for moving, stacking and
    splitting the nodes into the window.

    Attributes:
        name: Name of the window
        color_identifier: QColor associated with the window.
    """

    def __init__(
        self,
        default_node_panel_factory: "providers.Factory",
        name="NodesWindow",
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        self.name = name
        self.color_identifier = QColor.fromHsvF(random.random(), 0.65, 0.6)

        self.__default_node_panel_factory = default_node_panel_factory

        self.__node_panels = {}

        self.__background_widget = QWidget()
        self.__background_widget.setFixedWidth(0)
        self.setCentralWidget(self.__background_widget)

    def add_graphics_node(self, graphics_node: "GraphicsNode"):
        """Adds a new GraphicsNode to the window.

        The method will create a NodePanel object using the `default_node_panel_factory`
        and insert the GraphicsNode inside it.

        Also, GraphicsNode objects will add a reference to this NodesWindow object on
        their parent_node_windows list. (See GraphicsNode)

        Important:
            GraphicsNode objects CAN'T BE REPEATED. If the GraphicsNode is already
            present in another NodePanel, it won't be inserted again.

        """
        if graphics_node in self.__node_panels:
            return

        node_panel: "NodePanel" = self.__default_node_panel_factory(
            graphics_node, parent=self
        )
        graphics_node.parent_node_windows.append(self)

        self.__node_panels[graphics_node] = node_panel

        if len(self.__node_panels) % 2:
            self.addDockWidget(Qt.RightDockWidgetArea, node_panel)
        else:
            self.addDockWidget(Qt.LeftDockWidgetArea, node_panel)

    def remove_graphics_node(self, graphics_node: "GraphicsNode"):
        """Removes the GraphicsNode from the window.

        Doesn't do anything if the graphics_node is not present on the window.
        """
        if graphics_node not in self.__node_panels:
            return

        node_panel = self.__node_panels[graphics_node]
        self.removeDockWidget(node_panel)

    def clear(self):
        """Remove all GraphicsNode and NodePanel objects from this window."""
        for graphics_node in self.__node_panels.keys():
            try:
                graphics_node.parent_node_windows.remove(self)
                self.removeDockWidget(self.__node_panels[graphics_node])
            except ValueError:
                pass

        self.__node_panels.clear()


NodesWindowFactory = providers.Factory(NodesWindow, NodePanelFactory.delegate())
