# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import random

import dependency_injector.providers as providers
from dial_gui.node_editor import GraphicsNode
from PySide2.QtCore import Qt
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QMainWindow, QWidget

from .node_panel import NodePanelFactory


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

        self.__node_panels = {}

        self.color_identifier = QColor.fromHsvF(random.random(), 0.65, 0.6)

        self.setCentralWidget(QWidget())

    def add_graphics_node(self, graphics_node: "GraphicsNode"):
        if graphics_node in self.__node_panels:
            return

        node_panel = self.__node_panel_factory(graphics_node, parent=self)

        self.__node_panels[graphics_node] = node_panel
        graphics_node.parent_node_windows.append(self)

        if len(self.__node_panels) % 2:
            self.addDockWidget(Qt.RightDockWidgetArea, node_panel)
        else:
            self.addDockWidget(Qt.LeftDockWidgetArea, node_panel)

    def remove_graphics_node(self, graphics_node: "GraphicsNode"):
        if graphics_node not in self.__node_panels:
            return

        node_panel = self.__node_panels[graphics_node]
        self.removeDockWidget(node_panel)

    def clear(self):
        for graphics_node in self.__node_panels.keys():
            try:
                graphics_node.parent_node_windows.remove(self)
            except ValueError:
                pass


NodesWindowFactory = providers.Factory(NodesWindow, NodePanelFactory.delegate())
