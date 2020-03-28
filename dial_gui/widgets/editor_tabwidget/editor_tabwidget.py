# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_gui.node_editor import NodeEditorWindowFactory
from dial_gui.widgets.node_panels import NodesWindow, NodesWindowsManagerSingleton
from PySide2.QtWidgets import QTabBar, QTabWidget

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget
    from dial_gui.node_editor import NodeEditorWindow
    from dial_gui.widgets.node_panels import NodesWindowsManager


class EditorTabWidget(QTabWidget):
    """The EditorTabWidget class provides a widget with a default NodeEditorWindow.

    It also can display NodePanelsWindow objects on tabs.
    """

    def __init__(
        self,
        node_editor_window: "NodeEditorWindow",
        nodes_windows_manager: "NodesWindowsManager",
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        self.__nodes_windows_manager = nodes_windows_manager
        self.__node_editor_window = node_editor_window

        self.setMovable(True)
        self.setTabsClosable(True)

        self.tabCloseRequested.connect(lambda index: self.removeTab(index))

        self.insertTab(0, self.__node_editor_window, "Editor")

        self.tabBar().tabButton(0, QTabBar.RightSide).deleteLater()
        self.tabBar().setTabButton(0, QTabBar.RightSide, None)

        self.__setup_connections()

    def __setup_connections(self):
        self.__nodes_windows_manager.nodes_window_added.connect(
            self.add_nodes_window_tab
        )
        self.__nodes_windows_manager.nodes_window_removed.connect(
            self.remove_nodes_window_tab
        )

    def add_nodes_window_tab(self, nodes_window: "NodesWindow"):
        self.addTab(nodes_window, nodes_window.name)

    def remove_nodes_window_tab(self, nodes_window: "NodesWindow"):
        index = self.indexOf(nodes_window)
        super().removeTab(index)

    def removeTab(self, index: int):
        widget = self.widget(index)
        if isinstance(widget, NodesWindow):
            self.__nodes_windows_manager.remove_nodes_window(widget)

    @property
    def node_editor_window(self) -> "NodeEditorWindow":
        return self.__node_editor_window


EditorTabWidgetFactory = providers.Factory(
    EditorTabWidget,
    nodes_windows_manager=NodesWindowsManagerSingleton,
    node_editor_window=NodeEditorWindowFactory,
)
