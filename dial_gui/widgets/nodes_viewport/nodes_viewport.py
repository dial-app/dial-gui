# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDockWidget, QMainWindow

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget
    from dial_gui.node_editor import GraphicsNode


class NodesViewport(QMainWindow):
    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)
        pass

    def add_graphics_node(self, graphics_node: "GraphicsNode"):
        print(graphics_node)
        print(graphics_node._proxy_widget.widget())

        dock = QDockWidget(graphics_node.title, self)

        widget = graphics_node._proxy_widget.widget()
        graphics_node._proxy_widget.setWidget(None)
        print(widget.parentWidget())
        dock.setWidget(widget)

        self.addDockWidget(Qt.RightDockWidgetArea, dock)


NodesViewportFactory = providers.Factory(NodesViewport)
