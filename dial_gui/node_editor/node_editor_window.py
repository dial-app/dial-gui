# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_gui.project import ProjectManagerGUISingleton
from PySide2.QtWidgets import QVBoxLayout, QWidget

from .node_editor_view import NodeEditorView

if TYPE_CHECKING:
    from dial_gui.project import ProjectGUI, ProjectManagerGUI


class NodeEditorWindow(QWidget):
    def __init__(
        self, project_manager_gui: "ProjectManagerGUI", parent: "QWidget" = None,
    ):
        super().__init__(parent)

        # Components
        self.__project_manager_gui = project_manager_gui

        # TODO: Change QWidget()
        self.__node_editor_view = NodeEditorView(QWidget(), parent=self)
        self.__node_editor_view.setParent(self)

        self.__graphics_scene = self.__project_manager_gui.active.graphics_scene

        self.__node_editor_view.setScene(self.__graphics_scene)

        self.__main_layout = QVBoxLayout()
        self.__main_layout.addWidget(self.__node_editor_view)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__main_layout)

        # Connections
        self.__project_manager_gui.active_project_changed.connect(
            self.__active_project_changed
        )

        self.__active_project_changed(self.__project_manager_gui.active)

    def __active_project_changed(self, project: "ProjectGUI"):
        self.__node_editor_view.disconnect(self.__graphics_scene)
        self.__node_editor_view.setScene(project.graphics_scene)


NodeEditorWindowFactory = providers.Factory(
    NodeEditorWindow, project_manager_gui=ProjectManagerGUISingleton
)
