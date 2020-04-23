# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_core.utils import log
from dial_gui.project import ProjectManagerGUISingleton
from dial_gui.utils import application
from dial_gui.widgets.editor_tabwidget import EditorTabWidgetFactory
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QMainWindow

from .main_menubar import MainMenuBarFactory

if TYPE_CHECKING:
    from dial_gui.widgets.editor_tabwidget import EditorTabWidget
    from PySide2.QtWidgets import QWidget
    from .main_menubar import MainMenuBar
    from dial_gui.project import ProjectManagerGUI


LOGGER = log.get_logger(__name__)


class MainWindow(QMainWindow):
    """The MainWindow class provides an entry point for the GUI.

    All widgets must be children of a MainWindow object.
    """

    def __init__(
        self,
        editor_tabwidget: "EditorTabWidget",
        main_menubar: "MainMenuBar",
        project_manager: "ProjectManagerGUI",
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        # Initialize widgets
        self.__project_manager = project_manager
        self.__project_manager.setParent(self)

        self.__main_menu_bar = main_menubar
        self.__main_menu_bar.setParent(self)

        self.__editor_tabwidget = editor_tabwidget

        # Set window title
        self.setWindowTitle(f"Dial {application.version()}")

        # Configure menu and status bars
        self.setMenuBar(self.__main_menu_bar)
        self.setStatusBar(self.statusBar())

        self.setCentralWidget(self.__editor_tabwidget)

        self.__main_menu_bar.quit.connect(self.close)

    def closeEvent(self, event):
        self.__project_manager.closeEvent(event)

        super().closeEvent(event)

    def sizeHint(self) -> "QSize":
        """Returns the size of the main window."""
        return QSize(1000, 800)


MainWindowFactory = providers.Factory(
    MainWindow,
    editor_tabwidget=EditorTabWidgetFactory,
    main_menubar=MainMenuBarFactory,
    project_manager=ProjectManagerGUISingleton,
)
