# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from PySide2.QtCore import QUrl
from PySide2.QtGui import QDesktopServices
from PySide2.QtWidgets import QAction, QMenu

from dial_gui.utils import application
from dial_gui.widgets.plugin import PluginManagerDialogFactory

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget
    from dial_gui.widgets.plugin import PluginManagerDialog


class PluginsMenu(QMenu):
    def __init__(
        self, plugin_manager_dialog: "PluginManagerDialog", parent: "QWidget" = None
    ):
        super().__init__("&Plugins", parent)

        self.__plugin_manager_dialog = plugin_manager_dialog

        self._open_plugin_manager_act = QAction("Open plugin manager...", self)
        self._open_plugin_manager_act.triggered.connect(self.__show_plugin_manager)

        self._open_plugins_directory_act = QAction(
            'Open "plugins" directory in explorer...', self
        )
        self._open_plugins_directory_act.triggered.connect(
            self.__open_plugins_directory
        )

        self.addAction(self._open_plugin_manager_act)
        self.addAction(self._open_plugins_directory_act)

    def __show_plugin_manager(self):
        self.__plugin_manager_dialog.show()

    def __open_plugins_directory(self):
        plugins_directory = application.plugins_directory()

        QDesktopServices.openUrl(QUrl(plugins_directory, QUrl.TolerantMode))


PluginsMenuFactory = providers.Factory(
    PluginsMenu, plugin_manager_dialog=PluginManagerDialogFactory
)
