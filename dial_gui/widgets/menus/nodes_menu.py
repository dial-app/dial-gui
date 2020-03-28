# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_core.node_editor import Node, NodeRegistrySingleton
from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QAction, QMenu

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget
    from dial_core.node_editor import NodeRegistry


class NodesMenu(QMenu):
    node_created = Signal(Node)

    def __init__(
        self, node_registry: "NodeRegistry", parent: "QWidget" = None,
    ):
        super().__init__("&Nodes", parent)

        self.setTearOffEnabled(True)

        for node_name, factory in node_registry.nodes.items():
            action = QAction(node_name, self)

            action.triggered.connect(
                lambda _=False, factory=factory: self.node_created.emit(factory())
            )

            self.addAction(action)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:  # Ignore right clicks
            return

        super().mouseReleaseEvent(event)


NodesMenuFactory = providers.Factory(NodesMenu, node_registry=NodeRegistrySingleton)
