# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from copy import deepcopy

from dial_core.project import Project
from dial_gui.node_editor import GraphicsScene


class ProjectGUI(Project):
    def __init__(self, name: str, graphics_scene: "GraphicsScene"):
        super().__init__(name, graphics_scene.scene)

        self.__graphics_scene = graphics_scene

    @property
    def graphics_scene(self):
        return self.__graphics_scene

