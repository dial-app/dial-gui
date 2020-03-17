# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtWidgets import QDialog
from PySide2.QtCore import QSize

import dependency_injector.providers as providers


class PluginManagerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Plugin Manager")

    def sizeHint(self) -> "QSize":
        """Preferred size of this dialog."""
        return QSize(800, 600)

PluginManagerDialogFactory = providers.Factory(PluginManagerDialog)
