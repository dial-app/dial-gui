# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_gui.node_editor import NodeEditorWindowFactory
from PySide2.QtWidgets import QTabBar, QTabWidget

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget
    from dial_gui.node_editor import NodeEditorWindow


class EditorTabWidget(QTabWidget):
    """The EditorTabWidget class provides a widget with a default NodeEditorWindow,
    along with some methods to add and manage NodesViewport objects.
    """

    def __init__(
        self, node_editor_window: "NodeEditorWindow", parent: "QWidget" = None,
    ):
        super().__init__(parent)

        self.__node_editor_window = node_editor_window

        self.setMovable(True)
        self.setTabsClosable(True)

        self.tabCloseRequested.connect(lambda index: self.removeTab(index))

        self.insertTab(0, self.__node_editor_window, "Editor")

        self.tabBar().tabButton(0, QTabBar.RightSide).deleteLater()
        self.tabBar().setTabButton(0, QTabBar.RightSide, None)

    @property
    def node_editor_window(self) -> "NodeEditorWindow":
        return self.__node_editor_window


EditorTabWidgetFactory = providers.Factory(
    EditorTabWidget, node_editor_window=NodeEditorWindowFactory
)
