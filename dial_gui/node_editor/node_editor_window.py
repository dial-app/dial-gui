# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from PySide2.QtWidgets import QVBoxLayout, QWidget

from dial_core.node_editor import Node

from .context_menu import DialContextMenu
from .node_editor_view import NodeEditorView

if TYPE_CHECKING:
    from PySide2.QtWidgets import QTabWidget
    from PySide2.QtGui import QContextMenuEvent
    from dial_core.project import ProjectManager
    from dial_gui.project import ProjectGUI


class NodeEditorWindow(QWidget):
    def __init__(
        self,
        tabs_widget: "QTabWidget",
        project_manager: "ProjectManager",
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        self.__project_manager = project_manager

        self.__main_layout = QVBoxLayout()

        self.__node_editor_view = NodeEditorView(tabs_widget, parent=self)
        self.__graphics_scene = self.__project_manager.active.graphics_scene

        self.__node_editor_view.setScene(self.__graphics_scene)

        self.__setup_ui()

        node = Node(title="hueheuheu")
        node.add_input_port(name="asdf", port_type=int)
        node.add_output_port(name="outut", port_type=str)

        node2 = Node(title="hahaha")
        node2.add_input_port(name="inn", port_type=str)
        node2.add_input_port(name="inn2", port_type=str)

        self.__graphics_scene.add_node_to_graphics(node)
        self.__graphics_scene.add_node_to_graphics(node2)

        self.__project_manager.active_project_changed.connect(
            self.__active_project_changed
        )

        self.show()
        self.__active_project_changed(self.__project_manager.active)

    def __setup_ui(self):
        """Sets the UI configuration."""
        self.__main_layout.addWidget(self.__node_editor_view)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__main_layout)

    def contextMenuEvent(self, event: "QContextMenuEvent"):
        menubar = DialContextMenu(
            parent=self,
            graphics_scene=self.__graphics_scene,
            project_manager=self.__project_manager,
            node_editor_view=self.__node_editor_view,
        )
        menubar.popup(event.globalPos())

    def __active_project_changed(self, project: "ProjectGUI"):
        self.__node_editor_view.disconnect(self.__graphics_scene)

        self.__node_editor_view.setScene(project.graphics_scene)

        self.__node_editor_view.connection_created.connect(
            self.__graphics_scene.add_graphics_connection
        )
        self.__node_editor_view.connection_removed.connect(
            self.__graphics_scene.remove_graphics_connection
        )
