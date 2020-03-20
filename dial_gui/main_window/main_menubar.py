# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_gui.widgets.menus import (
    FileMenuFactory,
    PluginsMenuFactory,
    ProjectsMenuFactory,
    WindowsMenuFactory,
)
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QMenuBar

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget
    from dial_gui.widgets.menus import FileMenu, PluginsMenu, WindowsMenu, ProjectsMenu


class MainMenuBar(QMenuBar):
    """
    Top menu bar for the main window.
    """

    quit = Signal()

    def __init__(
        self,
        file_menu: "FileMenu",
        plugins_menu: "PluginsMenu",
        windows_menu: "WindowsMenu",
        projects_menu: "ProjectsMenu",
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        self.__file_menu = file_menu
        self.__plugins_menu = plugins_menu
        self.__windows_menu = windows_menu
        self.__projects_menu = projects_menu

        # File menu
        self.addMenu(self.__file_menu)
        self.addMenu(self.__plugins_menu)
        self.addMenu(self.__windows_menu)
        self.addMenu(self.__projects_menu)

        self.__file_menu.quit.connect(lambda: self.quit.emit())


MainMenuBarFactory = providers.Factory(
    MainMenuBar,
    file_menu=FileMenuFactory,
    plugins_menu=PluginsMenuFactory,
    windows_menu=WindowsMenuFactory,
    projects_menu=ProjectsMenuFactory,
)
