# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers

from dial_core.project import Project
from dial_gui.node_editor import GraphicsSceneFactory


class ProjectGUI(Project):
    def __init__(self, name: str, graphics_scene: "GraphicsScene"):
        super().__init__(name, graphics_scene.scene)

        self.__graphics_scene = graphics_scene

    @property
    def graphics_scene(self):
        return self.__graphics_scene

    def __reduce__(self):
        return (ProjectGUI, (self.name, self.__graphics_scene))


ProjectGUIFactory = providers.Factory(
    ProjectGUI, name="Default Project", graphics_scene=GraphicsSceneFactory
)
