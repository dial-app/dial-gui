# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from PySide2.QtWidgets import QVBoxLayout, QWidget

from .node_editor_view import NodeEditorView

if TYPE_CHECKING:
    from PySide2.QtWidgets import QTabWidget
    from dial_core.project import ProjectManager
    from dial_gui.project import ProjectGUI


class NodeEditorWindow(QWidget):
    def __init__(
        self,
        tabs_widget: "QTabWidget",
        project_manager: "ProjectManager",
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        self.__project_manager = project_manager

        self.__main_layout = QVBoxLayout()

        self.__node_editor_view = NodeEditorView(tabs_widget, parent=self)
        self.__graphics_scene = self.__project_manager.active.graphics_scene

        self.__node_editor_view.setScene(self.__graphics_scene)

        self.__main_layout.addWidget(self.__node_editor_view)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__main_layout)

        self.__project_manager.active_project_changed.connect(
            self.__active_project_changed
        )

        self.show()
        self.__active_project_changed(self.__project_manager.active)

    def __active_project_changed(self, project: "ProjectGUI"):
        self.__node_editor_view.disconnect(self.__graphics_scene)
        self.__node_editor_view.setScene(project.graphics_scene)
