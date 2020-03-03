# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.providers as providers

from dial_gui.project import ProjectManagerGUISingleton
from dial_gui.widgets.log import LoggerDialogFactory

from .main_menubar import MainMenuBar
from .main_window import MainWindow

MainMenuBarFactory = providers.DelegatedFactory(MainMenuBar)

MainWindowFactory = providers.Factory(
    MainWindow,
    menubar_factory=MainMenuBarFactory,
    logger_dialog=LoggerDialogFactory,
    project_manager=ProjectManagerGUISingleton,
)
