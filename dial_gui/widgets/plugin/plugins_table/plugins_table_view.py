# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from PySide2.QtWidgets import QHeaderView, QTableView

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget


class PluginsTableView(QTableView):
    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.horizontalHeader().setStretchLastSection(True)


PluginsTableViewFactory = providers.Factory(PluginsTableView)
