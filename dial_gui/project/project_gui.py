# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from dial_core.project import Project
from dial_gui.node_editor import GraphicsScene


class ProjectGUI(Project):
    def __init__(self, name: str, graphics_scene: "GraphicsScene"):
        super().__init__(name, graphics_scene.scene)
