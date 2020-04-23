# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_core.project import Project
from dial_gui.node_editor import GraphicsSceneFactory
from dial_gui.node_editor.nodes_windows import NodesWindowsGroupFactory

if TYPE_CHECKING:
    from dial_gui.node_editor import GraphicsScene
    from dial_gui.node_editor.nodes_windows import NodesWindowsGroup


class ProjectGUI(Project):
    def __init__(
        self,
        name: str,
        graphics_scene: "GraphicsScene",
        nodes_windows_manager: "NodesWindowsGroup",
    ):
        super().__init__(name, graphics_scene.scene)

        self._graphics_scene = graphics_scene
        self._graphics_scene.scene.parent = self

        self._nodes_windows_manager = nodes_windows_manager

    @property
    def graphics_scene(self):
        return self._graphics_scene

    @property
    def nodes_windows_manager(self):
        return self._nodes_windows_manager

    def __reduce__(self):
        return (
            ProjectGUI,
            (self.name, self._graphics_scene, self._nodes_windows_manager,),
        )


ProjectGUIFactory = providers.Factory(
    ProjectGUI,
    name="Default Project",
    graphics_scene=GraphicsSceneFactory,
    nodes_windows_manager=NodesWindowsGroupFactory,
)
