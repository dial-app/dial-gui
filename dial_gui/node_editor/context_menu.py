# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from PySide2.QtWidgets import QMenu

from dial_core.node_editor import NodeFactorySingleton
from dial_gui.widgets.menus import FileMenu, NodesMenu

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget
    from dial_gui.node_editor import GraphicsScene, NodeEditorView
    from dial_core.project import ProjectManager


class DialContextMenu(QMenu):
    def __init__(
        self,
        graphics_scene: "GraphicsScene",
        node_editor_view: "NodeEditorView",
        project_manager: "ProjectManager",
        parent: "QWidget" = None,
    ):
        super().__init__("Menu", parent)

        self.addMenu(FileMenu(project_manager=project_manager, parent=self))
        self.addMenu(
            NodesMenu(
                node_factory=NodeFactorySingleton(),
                graphics_scene=graphics_scene,
                node_editor_view=node_editor_view,
            )
        )
