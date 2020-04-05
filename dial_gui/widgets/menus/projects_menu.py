# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_core.project import Project
from dial_core.utils import log
from dial_gui.project import ProjectManagerGUI, ProjectManagerGUISingleton
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QAction, QActionGroup, QMenu

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget

LOGGER = log.get_logger(__name__)


class ProjectsMenu(QMenu):
    """The ProjectsMenu class provides a menu with all the currently active project, and
    allows changing between them when clicking."""

    def __init__(
        self, project_manager: "ProjectManagerGUI", parent: "QWidget" = None
    ):
        super().__init__("Projects", parent)

        # Components
        self.__project_manager = project_manager

        # The menu is regenerated each time it needs to change: When a project is
        # opened, or when a project is removed
        self.__project_manager.project_added.connect(self.__add_project_to_menu)
        self.__project_manager.active_project_changed.connect(
            self.__set_active_project
        )
        self.__project_manager.project_removed.connect(
            lambda: self.__generate_menu_from_projects()
        )

        # Actions
        self.__projects_actions_group = QActionGroup(self)
        self.__generate_menu_from_projects()
        self.__set_active_project(self.__project_manager.active)

    def mouseReleaseEvent(self, event):
        """Ignores right clicks on the QMenu (Avoids unintentional clicks)"""
        if event.button() == Qt.RightButton:  # Ignore right clicks
            return

        super().mouseReleaseEvent(event)

    def __generate_menu_from_projects(self):
        """Adds an entry to the menu for each Project in the ProjectManagerGUI"""
        self.clear()
        for project in self.__project_manager.projects:
            self.__add_project_to_menu(project)

    def __add_project_to_menu(self, project: "Project"):
        """Creates a new entry for the passed project. Clicking on the project will make
        it the active project on the project manager."""
        project_action = QAction(project.name, self)
        project_action.setCheckable(True)

        index = self.__project_manager.projects.index(project)

        project_action.triggered.connect(
            lambda _=False, index=index: self.__project_manager.set_active_project(
                index
            )
        )

        self.__projects_actions_group.addAction(project_action)
        self.addAction(project_action)

        LOGGER.debug("Created ProjectMenu Action (Index %s): %s", index, project_action)

    def __set_active_project(self, project: "Project"):
        """Makes the passed project the active one on the menu (will be marked)."""
        index = self.__project_manager.projects.index(project)

        self.actions()[index].setChecked(True)

        LOGGER.debug("Project with index %s is now active on menu: %s", index, project)


ProjectsMenuFactory = providers.Factory(
    ProjectsMenu, project_manager=ProjectManagerGUISingleton
)
