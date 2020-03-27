# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_gui.widgets.nodes_viewport import NodesViewportFactory
from PySide2.QtWidgets import QAction, QMenu

from .graphics_node import GraphicsNode

if TYPE_CHECKING:
    from .node_editor_view import NodeEditorView
    from PySide2.QtWidgets import QTabWidget, QWidget


class NodeEditorViewMenu(QMenu):
    def __init__(
        self,
        tabs_widget: "QTabWidget",
        node_editor_view: "NodeEditorView",
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        self.__node_editor_view = node_editor_view
        self.__tabs_widget = tabs_widget

        self._remove_elements_act = QAction("Remove nodes", self)
        self._remove_elements_act.triggered.connect(self.__remove_selected_elements)

        self._add_nodes_to_new_viewport_act = QAction("Add nodes to new viewport", self)
        self._add_nodes_to_new_viewport_act.triggered.connect(
            self.__add_nodes_to_new_viewport
        )

        self._add_nodes_to_existing_viewport_menu = QMenu(
            "Add nodes to existing viewport...", self
        )
        # for viewport in self.node_editor_view.scene().selected_item():
        #     action = self._add_nodes_to_existing_viewport_menu.addAction("asdf")
        #     action.triggered.connect(
        #         lambda _=None, viewport=viewport: self.__add_nodes_to_existing_viewport(
        #             viewport
        #         )
        #     )

        self.addAction(self._remove_elements_act)
        self.addSeparator()
        self.addAction(self._add_nodes_to_new_viewport_act)
        self.addMenu(self._add_nodes_to_existing_viewport_menu)

    def __remove_selected_elements(self):
        for selected_item in self.__node_editor_view.scene().selectedItems():
            self.__node_editor_view.scene().removeItem(selected_item)

        self.__node_editor_view.scene().update()

    def __add_nodes_to_new_viewport(self):
        nodes_viewport = NodesViewportFactory(parent=self.__node_editor_view)
        self.__tabs_widget.addTab(nodes_viewport, "Viewport")

        for selected_item in self.__node_editor_view.scene().selectedItems():
            if isinstance(selected_item, GraphicsNode):
                nodes_viewport.add_graphics_node(selected_item)

    def __add_nodes_to_existing_viewport(self, viewport):
        print("ASDf")


NodeEditorViewMenuFactory = providers.Factory(NodeEditorViewMenu)
