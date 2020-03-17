# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers

from PySide2.QtWidgets import QMenu, QAction

from dial_gui.widgets.plugin import PluginManagerDialogFactory

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget

class PluginsMenu(QMenu):
    def __init__( self, plugin_manager_dialog: "PluginManagerDialog", parent: "QWidget"=None):
        super().__init__("&Plugins", parent)

        self.__plugin_manager_dialog = plugin_manager_dialog


        self._open_plugin_manager = QAction("Open plugin manager...", self)
        self._open_plugin_manager.triggered.connect(self.__toggle_plugin_manager)

        self.addAction(self._open_plugin_manager)


    def __toggle_plugin_manager(self):
        self.__plugin_manager_dialog.show()


PluginsMenuFactory = providers.Factory(PluginsMenu,
                                       plugin_manager_dialog=PluginManagerDialogFactory)
