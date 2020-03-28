# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_gui.widgets.log import LoggerDialogFactory
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QAction, QMenu

if TYPE_CHECKING:
    from dial_gui.widgets.log import LoggerDialog
    from PySide2.QtWidgets import QWidget


class WindowsMenu(QMenu):
    def __init__(self, logger_dialog: "LoggerDialog", parent: "QWidget" = None):
        super().__init__("&Windows", parent)

        self.__logger_dialog = logger_dialog

        self._show_log_act = QAction("Show log", self)
        self._show_log_act.triggered.connect(self.__toggle_logger_dialog)

        self.addAction(self._show_log_act)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:  # Ignore right clicks
            return

        super().mouseReleaseEvent(event)

    def __toggle_logger_dialog(self):
        self.__logger_dialog.show()


WindowsMenuFactory = providers.Factory(WindowsMenu, logger_dialog=LoggerDialogFactory)
