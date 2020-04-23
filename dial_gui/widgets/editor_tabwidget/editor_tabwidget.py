# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_gui.widgets.node_editor import NodeEditorWindowFactory
from dial_gui.node_editor.nodes_windows import NodesWindow
from dial_gui.project import ProjectManagerGUISingleton
from PySide2.QtCore import QEvent
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QStackedWidget, QTabBar, QTabWidget, QWidget

from .tab_settings_dialog import TabSettingsDialog

if TYPE_CHECKING:
    from dial_gui.project import ProjectManagerGUI
    from dial_gui.node_editor.nodes_windows import NodesWindowsGroup


class CustomTabWidget(QTabWidget):
    def __init__(
        self, nodes_windows_manager: "NodesWindowsGroup", parent: "QWidget" = None,
    ):
        super().__init__(parent)

        self.__nodes_windows_manager = nodes_windows_manager

        self.setMovable(True)
        self.setTabsClosable(True)
        self.tabBar().installEventFilter(self)

        self.tabCloseRequested.connect(lambda index: self.removeTab(index))

        self.__setup_connection()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonDblClick:
            index = obj.tabAt(event.pos())
            widget = self.widget(index)

            if isinstance(widget, NodesWindow):
                self.__tab_renamer_dialog = TabSettingsDialog(
                    index=index,
                    name=widget.name,
                    color=widget.color_identifier,
                    parent=self,
                )
                self.__tab_renamer_dialog.color_changed.connect(
                    self.__tab_color_changed
                )
                self.__tab_renamer_dialog.name_changed.connect(
                    self.__tab_name_changed
                )
                self.__tab_renamer_dialog.show()

        return super().eventFilter(obj, event)

    def __tab_color_changed(self, index, color):
        nodes_window = self.widget(index)

        if not nodes_window:
            return

        nodes_window.color_identifier = color

        square_pixmap = QPixmap(16, 16)
        square_pixmap.fill(nodes_window.color_identifier)
        self.setTabIcon(index, QIcon(square_pixmap))

    def __tab_name_changed(self, index, name):
        nodes_window = self.widget(index)

        if not nodes_window:
            return

        nodes_window.name = name
        self.setTabText(index, name)

    def __setup_connection(self):
        self.__nodes_windows_manager.nodes_window_added.connect(
            self.add_nodes_window_tab
        )

        self.__nodes_windows_manager.nodes_window_removed.connect(
            self.remove_nodes_window_tab
        )

    def add_nodes_window_tab(self, nodes_window: "NodesWindow"):
        square_pixmap = QPixmap(16, 16)
        square_pixmap.fill(nodes_window.color_identifier)
        self.addTab(nodes_window, QIcon(square_pixmap), nodes_window.name)

    def remove_nodes_window_tab(self, nodes_window: "NodesWindow"):
        index = self.indexOf(nodes_window)
        super().removeTab(index)

    def removeTab(self, index: int):
        widget = self.widget(index)
        if isinstance(widget, NodesWindow):
            self.__nodes_windows_manager.remove_nodes_window(widget)


class EditorTabWidget(QStackedWidget):
    """The EditorTabWidget class provides a widget with a default NodeEditorWindow.

    It also can display NodePanelsWindow objects on tabs.
    """

    def __init__(
        self,
        project_manager: "ProjectManagerGUI",
        node_editor_window_factory: "providers.Factory",
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        self.__project_manager = project_manager

        self.__node_editor_window = node_editor_window_factory(
            graphics_scene=self.__project_manager.active.graphics_scene
        )
        self.__node_editor_window.setParent(self)

        self.__new_tabs_widget(self.__project_manager.active.nodes_windows_manager)
        self.setCurrentIndex(0)

        self.__setup_connections()

    @property
    def node_editor_window(self):
        return self.__node_editor_window

    def __new_tabs_widget(self, nodes_windows_manager):
        tabs_widget = CustomTabWidget(
            nodes_windows_manager=nodes_windows_manager, parent=self,
        )
        self.addWidget(tabs_widget)

    def __setup_connections(self):
        self.__project_manager.project_added.connect(
            lambda project: self.__new_tabs_widget(project.nodes_windows_manager)
        )
        self.__project_manager.active_project_changed.connect(
            lambda project: self.setCurrentIndex(
                self.__project_manager.index_of(project)
            )
        )

        self.__project_manager.active_project_changed.connect(
            lambda project: self.__node_editor_window.change_graphics_scene(
                project.graphics_scene
            )
        )

        self.__project_manager.project_removed.connect(
            lambda project, index: self.removeWidget(self.widget(index))
        )

    def setCurrentIndex(self, index: int):
        super().setCurrentIndex(index)

        tabs_widget = self.currentWidget()

        if not tabs_widget:
            return

        tabs_widget.insertTab(0, self.__node_editor_window, "Editor")
        tabs_widget.tabBar().tabButton(0, QTabBar.RightSide).deleteLater()
        tabs_widget.tabBar().setTabButton(0, QTabBar.RightSide, None)
        tabs_widget.setCurrentIndex(0)


EditorTabWidgetFactory = providers.Factory(
    EditorTabWidget,
    node_editor_window_factory=NodeEditorWindowFactory.delegate(),
    project_manager=ProjectManagerGUISingleton,
)
