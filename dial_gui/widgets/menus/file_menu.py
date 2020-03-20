# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_gui.project import ProjectManagerGUISingleton
from PySide2.QtCore import Signal
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QAction, QMenu

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget
    from dial_core.project import ProjectManager


class FileMenu(QMenu):
    """The class FileMenu provides a configured menu for the basic File operations
    (Open/Close/Save projects, exit program...)."""

    quit = Signal()

    def __init__(self, project_manager: "ProjectManager", parent: "QWidget" = None):
        super().__init__("&File", parent)

        self.__project_manager = project_manager

        # Add actions
        self._new_project_act = QAction("New project", self)
        self._new_project_act.setShortcut(QKeySequence.New)
        self._new_project_act.triggered.connect(self.__project_manager.new_project)

        self._open_project_act = QAction("Open project", self)
        self._open_project_act.setShortcut(QKeySequence.Open)
        self._open_project_act.triggered.connect(self.__project_manager.open_project)

        self._save_project_act = QAction("Save project", self)
        self._save_project_act.setShortcut(QKeySequence.Save)
        self._save_project_act.triggered.connect(
            lambda: self.__project_manager.save_project(self.__project_manager.active)
        )

        self._save_project_as_act = QAction("Save project as...", self)
        self._save_project_as_act.triggered.connect(
            lambda: self.__project_manager.save_project_as(
                self.__project_manager.active
            )
        )

        self._close_project_act = QAction("Close project", self)
        self._close_project_act.triggered.connect(
            lambda: self.__project_manager.close_project(self.__project_manager.active)
        )

        self._quit_act = QAction("Quit", self)
        self._quit_act.setShortcut(QKeySequence.Quit)
        self._quit_act.triggered.connect(lambda: self.quit.emit())

        # Configure menu
        self.addAction(self._new_project_act)
        self.addAction(self._open_project_act)
        self.addAction(self._save_project_act)
        self.addAction(self._save_project_as_act)
        self.addAction(self._close_project_act)
        self.addSeparator()
        self.addAction(self._quit_act)


FileMenuFactory = providers.Factory(
    FileMenu, project_manager=ProjectManagerGUISingleton
)
