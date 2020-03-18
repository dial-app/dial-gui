# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QDialog, QVBoxLayout, QGroupBox

from dial_gui.widgets.log import LoggerTextboxFactory
from dial_core.utils import log
import logging

from .plugins_table import PluginsTableWidgetFactory

if TYPE_CHECKING:
    from .plugins_table import PluginsTableWidget


class PluginManagerDialog(QDialog):
    def __init__(self, plugins_table_widget: "PluginsTableWidget", parent=None):
        super().__init__(parent)

        self.setWindowTitle("Plugin Manager")

        self.__plugins_table_widget = plugins_table_widget
        self.__plugins_table_widget.setParent(self)

        self.__actions_output_textarea = LoggerTextboxFactory(
            formatter=logging.Formatter(
                "%(asctime)s - %(levelname)s: %(message)s", "%H:%M:%S"
            ),
            parent=self,
        )
        log.get_logger("plugins").addHandler(self.__actions_output_textarea)

        self.__main_layout = QVBoxLayout()

        actions_output_group = QGroupBox("Commands output")
        actions_output_layout = QVBoxLayout()
        actions_output_layout.addWidget(self.__actions_output_textarea)
        actions_output_group.setLayout(actions_output_layout)

        self.__main_layout.addWidget(self.__plugins_table_widget)
        self.__main_layout.addWidget(actions_output_group)

        self.setLayout(self.__main_layout)

    def sizeHint(self) -> "QSize":
        """Preferred size of this dialog."""
        return QSize(600, 400)


PluginManagerDialogFactory = providers.Factory(
    PluginManagerDialog, plugins_table_widget=PluginsTableWidgetFactory
)
