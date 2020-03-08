# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from dial_core.project import Project
from dial_gui.node_editor import GraphicsScene


class ProjectGUI(Project):
    def __init__(self, name: str, graphics_scene: "GraphicsScene"):
        super().__init__(name, graphics_scene.scene)

        self.__graphics_scene = graphics_scene

    @property
    def graphics_scene(self):
        return self.__graphics_scene

    def __getstate__(self):
        return {"name": self.name, "graphics_scene": self.__graphics_scene}

    def __setstate__(self, new_state):
        self.__init__(new_state["name"], new_state["graphics_scene"])
