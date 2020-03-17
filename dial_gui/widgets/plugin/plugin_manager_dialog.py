# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QDialog, QHBoxLayout

from .plugins_table import PluginsTableWidgetFactory

if TYPE_CHECKING:
    from .plugins_table import PluginsTableWidget


class PluginManagerDialog(QDialog):
    def __init__(self, plugins_table_widget: "PluginsTableWidget", parent=None):
        super().__init__(parent)

        self.setWindowTitle("Plugin Manager")

        self.__plugins_table_widget = plugins_table_widget
        self.__plugins_table_widget.setParent(self)

        self.__main_layout = QHBoxLayout()
        # self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.__main_layout.addWidget(self.__plugins_table_widget)

        self.setLayout(self.__main_layout)

    def sizeHint(self) -> "QSize":
        """Preferred size of this dialog."""
        return QSize(500, 300)


PluginManagerDialogFactory = providers.Factory(
    PluginManagerDialog, plugins_table_widget=PluginsTableWidgetFactory
)
