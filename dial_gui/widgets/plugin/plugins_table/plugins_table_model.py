# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import IntEnum
from typing import TYPE_CHECKING, Optional, Any

import dependency_injector.providers as providers
from PySide2.QtCore import QAbstractTableModel, QModelIndex, QSize, Qt
from dial_gui.utils import application

from dial_core.plugin import PluginManagerSingleton
from dial_core.utils import log

if TYPE_CHECKING:
    from PySide2.QtWidgets import QObject
    from dial_core.plugin import PluginManager, Plugin


class PluginsTableModel(QAbstractTableModel):
    class ColumnLabel(IntEnum):
        Active = 0
        Name = 1
        Summary = 2
        Version = 3

    def __init__(self, plugin_manager: "PluginManager", parent: "QObject" = None):
        super().__init__(parent)

        self.__plugin_manager = plugin_manager

        self.__role_map = {
            Qt.DisplayRole: self.__data_display_role,
            Qt.CheckStateRole: self.__data_checkstate_role,
            Qt.TextAlignmentRole: self.__data_textalignment_role,
            Qt.SizeHintRole: self.__data_sizehint_role,
        }

    def rowCount(self, parent=QModelIndex()):
        return len(self.__plugin_manager.installed_plugins)

    def columnCount(self, parent=QModelIndex()):
        return len(self.ColumnLabel)

    def index(self, row: int, column: int, parent: "QModelIndex") -> "QModelIndex":
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        return self.createIndex(
            row, column, list(self.__plugin_manager.installed_plugins.values())[row]
        )

    def flags(self, index: "QModelIndex") -> int:
        general_flags = super().flags(index)

        if index.column() == self.ColumnLabel.Active:
            return general_flags | Qt.ItemIsUserCheckable

        return general_flags

    def headerData(
        self, section: int, orientation: "Qt.Orientation", role=Qt.DisplayRole
    ) -> Optional[str]:

        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self.ColumnLabel(section).name

        return None

    def data(self, index: "QModelIndex", role=Qt.DisplayRole):
        if role in self.__role_map:
            return self.__role_map[role](index)

        return None

    def setData(
        self, index: "QModelIndex", value: Any, role: int = Qt.EditRole
    ) -> bool:
        if not index.isValid():
            return False

        plugin: "Plugin" = index.internalPointer()

        if role == Qt.CheckStateRole:
            if index.column() == self.ColumnLabel.Active:
                plugin.active = bool(value)

                log.get_logger("plugins").info(
                    f'Plugin "{plugin.name}" has been '
                    f"{'activated' if plugin.active else 'deactivated'}."
                )

        return True

    def __data_display_role(self, index: "QModelIndex") -> Optional["str"]:
        if not index.isValid():
            return None

        plugin: "Plugin" = index.internalPointer()

        if index.column() == self.ColumnLabel.Name:
            return plugin.name

        if index.column() == self.ColumnLabel.Summary:
            return plugin.summary

        if index.column() == self.ColumnLabel.Version:
            return plugin.version

        return None

    def __data_checkstate_role(self, index: "QModelIndex") -> Optional["Qt.CheckState"]:
        if not index.isValid():
            return None

        plugin: "Plugin" = index.internalPointer()

        if index.flags() & Qt.ItemIsUserCheckable:
            return Qt.Checked if plugin.active else Qt.Unchecked

        return None

    def __data_textalignment_role(self, index: "QModelIndex"):
        if not index.isValid():
            return None

        if index.column() == self.ColumnLabel.Version:
            return Qt.AlignCenter

        return None

    def __data_sizehint_role(self, index: "QModelIndex"):
        if not index.isValid():
            return None

        if index.column() == self.ColumnLabel.Active:
            return QSize(0, 0)

        return None


PluginsTableModelFactory = providers.Factory(
    PluginsTableModel,
    plugin_manager=PluginManagerSingleton(
        installed_plugins_dict=application.installed_plugins_file_content()
    ),
)
