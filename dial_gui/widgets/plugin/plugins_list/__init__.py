# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from PySide2.QtWidgets import QListWidget

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget


class PluginsList(QListWidget):
    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)
