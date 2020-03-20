# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_core.utils import log
from dial_gui.node_editor import NodeEditorWindow
from dial_gui.project import ProjectManagerGUISingleton
from dial_gui.utils import application
from dial_gui.widgets.log import LoggerDialogFactory
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QMainWindow, QTabBar, QTabWidget

from .main_menubar import MainMenuBarFactory

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget


LOGGER = log.get_logger(__name__)


class MainWindow(QMainWindow):
    """The main window for the program."""

    def __init__(
        self, main_menubar, project_manager, parent: "QWidget" = None,
    ):
        super().__init__(parent)

        # Initialize widgets
        self.__project_manager = project_manager
        self.__project_manager.setParent(self)

        self.__main_menu_bar = main_menubar
        self.__main_menu_bar.setParent(self)

        self.__tabs_widget = QTabWidget(self)
        self.__node_editor = NodeEditorWindow(
            tabs_widget=self.__tabs_widget,
            project_manager=self.__project_manager,
            parent=self,
        )

        # Configure ui
        self.__setup_ui()

        self.__main_menu_bar.quit.connect(self.close)

    def __setup_ui(self):
        # Set window title
        self.setWindowTitle(f"Dial {application.version()}")

        # Configure menu and status bars
        self.setMenuBar(self.__main_menu_bar)
        self.setStatusBar(self.statusBar())

        self.setCentralWidget(self.__tabs_widget)

        self.__tabs_widget.setMovable(True)
        self.__tabs_widget.setTabsClosable(True)

        self.__tabs_widget.tabCloseRequested.connect(
            lambda index: self.__tabs_widget.removeTab(index)
        )

        self.__tabs_widget.addTab(self.__node_editor, "Editor")

        # Remove "delete" button from the tab
        self.__tabs_widget.tabBar().tabButton(0, QTabBar.RightSide).deleteLater()
        self.__tabs_widget.tabBar().setTabButton(0, QTabBar.RightSide, None)

    def closeEvent(self, event):
        print("Main Menu close")
        self.__project_manager.closeEvent(event)

        super().closeEvent(event)

    def sizeHint(self) -> "QSize":
        """Returns the size of the main window."""
        return QSize(1000, 800)


MainWindowFactory = providers.Factory(
    MainWindow,
    main_menubar=MainMenuBarFactory,
    project_manager=ProjectManagerGUISingleton,
)
