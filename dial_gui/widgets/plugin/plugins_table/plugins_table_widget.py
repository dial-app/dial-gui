# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from PySide2.QtWidgets import QVBoxLayout, QWidget

from .plugins_table_model import PluginsTableModelFactory
from .plugins_table_view import PluginsTableViewFactory

if TYPE_CHECKING:
    from .plugins_table_model import PluginsTableModel
    from .plugins_table_view import PluginsTableView


class PluginsTableWidget(QWidget):
    def __init__(
        self,
        plugins_table_model: "PluginsTableModel",
        plugins_table_view: "PluginsTableView",
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        self.__plugins_table_model = plugins_table_model
        self.__plugins_table_model.setParent(self)

        self.__plugins_table_view = plugins_table_view
        self.__plugins_table_view.setParent(self)

        self.__plugins_table_view.setModel(self.__plugins_table_model)

        self.__main_layout = QVBoxLayout()
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.__main_layout.addWidget(self.__plugins_table_view)

        self.setLayout(self.__main_layout)


PluginsTableWidgetFactory = providers.Factory(
    PluginsTableWidget,
    plugins_table_model=PluginsTableModelFactory,
    plugins_table_view=PluginsTableViewFactory,
)
