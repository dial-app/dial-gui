# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from PySide2.QtWidgets import QAction, QMenu

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget
    from .node_editor_view import NodeEditorView


class NodeEditorViewMenu(QMenu):
    def __init__(self, node_editor_view: "NodeEditorView", parent: "QWidget" = None):
        super().__init__(parent)

        self.__node_editor_view = node_editor_view

        self._remove_elements_act = QAction("Remove selected nodes")
        self._remove_elements_act.triggered.connect(self.__remove_selected_elements)

        self._add_selected_nodes_to_viewport = QAction("Add selected nodes to viewport")
        self._add_selected_nodes_to_viewport.trigger.connect(
            self.__add_selected_nodes_to_viewport
        )

        self.addAction(self._remove_elements_act)

    def __remove_selected_elements(self):
        for selected_item in self.__node_editor_view.scene().selectedItems():
            self.__node_editor_view.scene().removeItem(selected_item)

        self.__node_editor_view.scene().update()


NodeEditorViewMenuFactory = providers.Factory(NodeEditorViewMenu)
