# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import os

import dependency_injector.providers as providers
from dial_core.project import ProjectManager
from dial_core.utils import log
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QFileDialog, QMessageBox, QWidget

from .project_gui import ProjectGUI, ProjectGUIFactory

LOGGER = log.get_logger(__name__)


class ProjectManagerGUI(QWidget, ProjectManager):
    new_project_created = Signal(ProjectGUI)
    project_added = Signal(ProjectGUI)
    active_project_changed = Signal(ProjectGUI)
    project_removed = Signal(ProjectGUI, int)

    def __init__(self, default_project: "ProjectGUI", parent=None):
        QWidget.__init__(self, parent)
        ProjectManager.__init__(self, default_project)

    def open_project(self):
        LOGGER.debug("Opening dialog for pickling a file...")

        file_path = QFileDialog.getOpenFileName(
            QWidget(), "Open Dial project", "", "Dial Files (*.dial)"
        )[0]
        LOGGER.info("File path selected for opening: %s", file_path)

        if file_path:
            super().open_project(file_path)
        else:
            LOGGER.info("Invalid file path. Loading cancelled.")

    def save_project(self, project: "ProjectGUI") -> "ProjectGUI":
        try:
            return super().save_project(project)

        except ValueError:
            LOGGER.warning("Project doesn't have a file path set!")
            return self.save_project_as(project)

    def save_project_as(self, project: "ProjectGUI"):
        LOGGER.debug("Opening dialog for picking a save file...")

        selected_parent_dir = QFileDialog.getExistingDirectory(
            parent=self,
            caption="Save Dial project",
            options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )

        # Avoid saving a project as a subproject
        if os.path.basename(selected_parent_dir) == project.name:
            selected_parent_dir = os.path.dirname(selected_parent_dir)

        LOGGER.info("File path selected for saving: %s", selected_parent_dir)

        if selected_parent_dir:
            super().save_project_as(project, selected_parent_dir)
        else:
            LOGGER.info("Invalid file path. Saving cancelled.")

    def close_project(self, project: "ProjectGUI"):
        return_code = QMessageBox.warning(
            self,
            "The document has been modified",
            "Do you want to save your changes?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
        )

        if return_code == QMessageBox.Cancel:
            return

        if return_code == QMessageBox.Save:
            self.save_project(project)

        # The project is closed if we discard the project or we save it
        super().close_project(project)

    def closeEvent(self, event):
        for project in list(self.projects):
            self.close_project(project)

    def _new_project_impl(self) -> "ProjectGUI":
        new_project = super()._new_project_impl()
        self.new_project_created.emit(new_project)
        return new_project

    def _add_project_impl(self, project: "ProjectGUI") -> "ProjectGUI":
        super()._add_project_impl(project)
        project.index = self.projects_count() - 1

        self.project_added.emit(project)
        return project

    def _set_active_project_impl(self, index: int) -> "ProjectGUI":
        active_project = super()._set_active_project_impl(index)
        self.active_project_changed.emit(active_project)
        return active_project

    def _remove_project_impl(self, project: "ProjectGUI") -> "ProjectGUI":
        index = self.index_of(project)
        super()._remove_project_impl(project)

        self.project_removed.emit(project, index)

        return project


ProjectManagerGUISingleton = providers.Singleton(
    ProjectManagerGUI, default_project=ProjectGUIFactory
)
