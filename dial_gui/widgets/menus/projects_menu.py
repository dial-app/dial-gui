# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers

from typing import TYPE_CHECKING

from dial_core.project import Project
from dial_gui.project import ProjectManagerGUI, ProjectManagerGUISingleton

from PySide2.QtWidgets import QMenu, QActionGroup, QAction
from dial_core.utils import log

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget

LOGGER = log.get_logger(__name__)


class ProjectsMenu(QMenu):
    def __init__(
        self, project_manager_gui: "ProjectManagerGUI", parent: "QWidget" = None
    ):
        super().__init__("Projects", parent)

        self.__project_manager_gui = project_manager_gui
        self.__project_manager_gui.project_added.connect(self.__add_project_to_menu)
        self.__project_manager_gui.active_project_changed.connect(
            self.__check_active_project
        )
        self.__project_manager_gui.project_removed.connect(
            lambda: self.__generate_menu_from_projects()
        )

        self.__projects_actions_group = QActionGroup(self)

        self.__generate_menu_from_projects()
        self.__check_active_project(self.__project_manager_gui.active)

    def __generate_menu_from_projects(self):
        self.clear()

        for project in self.__project_manager_gui.projects:
            self.__add_project_to_menu(project)

    def __add_project_to_menu(self, project: "Project"):
        project_action = QAction(project.name, self)
        project_action.setCheckable(True)

        index = self.__project_manager_gui.projects.index(project)

        project_action.triggered.connect(
            lambda _=False, index=index: self.__project_manager_gui.set_active_project(
                index
            )
        )

        self.__projects_actions_group.addAction(project_action)
        self.addAction(project_action)

        LOGGER.debug("Created ProjectMenu Action (Index %s): %s", index, project_action)

    def __check_active_project(self, project: "Project"):
        index = self.__project_manager_gui.projects.index(project)

        self.actions()[index].setChecked(True)

        LOGGER.debug("Project with index %s is now active on menu: %s", index, project)


ProjectsMenuFactory = providers.Factory(
    ProjectsMenu, project_manager_gui=ProjectManagerGUISingleton
)
