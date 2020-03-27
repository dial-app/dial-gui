# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:
import random
from typing import TYPE_CHECKING, List

import dependency_injector.providers as providers
from PySide2.QtCore import QEvent, Qt
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QDialog, QDockWidget, QMainWindow, QVBoxLayout, QWidget

if TYPE_CHECKING:
    from dial_gui.node_editor import GraphicsNode


class ViewportNodeBlock(QDockWidget):
    def __init__(self, graphics_node: "GraphicsNode", parent: "QWidget" = None):
        super().__init__(graphics_node.title, parent)

        self.__graphics_node = graphics_node

        self.__proxy_widget = self.__graphics_node._proxy_widget

        self.__inner_widget = self.__proxy_widget.widget()
        self.__last_size = self.__inner_widget.size()

    def event(self, event: "QEvent"):
        if event.type() == QEvent.Show:
            self.enable()
            return True

        if event.type() == QEvent.Hide:
            self.disable()
            return True

        return super().event(event)

    def enable(self):
        self.__last_size = self.__inner_widget.size()

        self.__graphics_node.set_inner_widget(QWidget())

        self.setWidget(self.__inner_widget)

    def disable(self):
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


class NodesViewport(QMainWindow):
    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        self.__node_blocks: List["ViewportNodeBlock"] = []

        self.color_identifier = QColor.fromHsvF(random.random(), 0.65, 0.6)

        self.setCentralWidget(QWidget())

    def add_graphics_node(self, graphics_node: "GraphicsNode"):
        viewport_node_block = ViewportNodeBlock(graphics_node, parent=self)
        self.__node_blocks.append(viewport_node_block)
        graphics_node.parent_viewports.append(self)

        if len(self.__node_blocks) % 2:
            self.addDockWidget(Qt.RightDockWidgetArea, viewport_node_block)
        else:
            self.addDockWidget(Qt.LeftDockWidgetArea, viewport_node_block)


NodesViewportFactory = providers.Factory(NodesViewport)
