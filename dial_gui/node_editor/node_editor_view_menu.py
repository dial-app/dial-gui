# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers

from typing import TYPE_CHECKING

from PySide2.QtWidgets import QMenu, QAction

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget
    from .node_editor_view import NodeEditorView


class NodeEditorViewMenu(QMenu):
    def __init__(self, node_editor_view: "NodeEditorView", parent: "QWidget" = None):
        super().__init__(parent)

        self.__node_editor_view = node_editor_view

        self._remove_elements = QAction("Remove selected elements")
        self._remove_elements.triggered.connect(self.__remove_selected_elements)

        self.addAction(self._remove_elements)

    def __remove_selected_elements(self):
        for selected_item in self.__node_editor_view.scene().selectedItems():
            self.__node_editor_view.scene().removeItem(selected_item)

        self.__node_editor_view.scene().update()


NodeEditorViewMenuFactory = providers.Factory(NodeEditorViewMenu)
