# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_gui.widgets.log import LoggerDialogFactory
from dial_gui.widgets.notebook_editor import (
    NotebookEditorDialog,
    NotebookEditorDialogFactory,
)
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QAction, QMenu

if TYPE_CHECKING:
    from dial_gui.widgets.log import LoggerDialog
    from PySide2.QtWidgets import QWidget


class WindowsMenu(QMenu):
    """The WindowsMenu class providers a menu with some windows (dialogs) that can be
    pop up. For example, a window with all the log."""

    def __init__(
        self,
        logger_dialog: "LoggerDialog",
        notebook_editor_dialog: "NotebookEditorDialog",
        parent: "QWidget" = None,
    ):
        super().__init__("&Windows", parent)

        self.__logger_dialog = logger_dialog
        self.__notebook_editor_dialog = notebook_editor_dialog

        self._show_log_act = QAction("Show log", self)
        self._show_log_act.triggered.connect(self.__toggle_logger_dialog)

        self._show_notebook_editor_act = QAction("Show Notebook Editor", self)
        self._show_notebook_editor_act.triggered.connect(
            self.__toggle_notebook_editor_dialog
        )

        self.addAction(self._show_log_act)
        self.addAction(self._show_notebook_editor_act)

    def mouseReleaseEvent(self, event):
        """Ignores right clicks on the QMenu (Avoids unintentional clicks)"""
        if event.button() == Qt.RightButton:  # Ignore right clicks
            return

        super().mouseReleaseEvent(event)

    def __toggle_logger_dialog(self):
        """Shows the log dialog window."""
        self.__logger_dialog.show()

    def __toggle_notebook_editor_dialog(self):
        """Shows the notebook editor window."""
        self.__notebook_editor_dialog.show()


WindowsMenuFactory = providers.Factory(
    WindowsMenu,
    logger_dialog=LoggerDialogFactory,
    notebook_editor_dialog=NotebookEditorDialogFactory,
)
