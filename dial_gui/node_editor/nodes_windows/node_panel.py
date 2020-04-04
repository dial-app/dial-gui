# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:
from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from PySide2.QtCore import QEvent
from PySide2.QtWidgets import QDialog, QDockWidget, QVBoxLayout, QWidget

if TYPE_CHECKING:
    from dial_gui.node_editor import GraphicsNode


class NodePanel(QDockWidget):
    """The NodePanel class allows a GraphicsNode to be correctly displayed inside a
    NodesWindow.

    Attributes:
        graphics_node: Related GraphicsNode object.
    """

    def __init__(self, graphics_node: "GraphicsNode", parent: "QWidget" = None):
        super().__init__(graphics_node.title, parent)

        self.__graphics_node = graphics_node

        self.__proxy_widget = self.__graphics_node._proxy_widget

        self.__inner_widget = self.__proxy_widget.widget()
        self.__last_size = self.__inner_widget.size()

    @property
    def graphics_node(self) -> "GraphicsNode":
        """Returns the GraphicsNode associated with this NodePanel."""
        return self.__graphics_node

    def event(self, event: "QEvent"):
        """Catches the show and hide events for the NodePanel.

        Important:
            Due to the system used for displaying the inner widgets on the Node Editor,
            a widget can't be displayed in two places at the same time, sharing
            ownership.

            Thus, every time this widget is show, the panel will catch the ownership of
            the GraphicsNode inner widget, and make it visible here.
            On the other side, when this panel is hidden, the ownership will be restored
            to the GraphicsNode.
        """
        if event.type() == QEvent.Show:
            self.__enable()
            return True

        if event.type() == QEvent.Hide:
            self.__disable()
            return True

        return super().event(event)

    def __enable(self):
        """Steals the ownership of the GraphicsNode's inner widget for correct
        visualization here."""
        self.__last_size = self.__inner_widget.size()

        self.__graphics_node.set_inner_widget(QWidget())

        self.setWidget(self.__inner_widget)

    def __disable(self):
        """Restores the ownership of the inner widget to its GraphicsNode."""
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


NodePanelFactory = providers.Factory(NodePanel)
