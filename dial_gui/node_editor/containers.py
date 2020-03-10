# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.providers as providers

from dial_core.node_editor import DefaultSceneFactory

from .graphics_port import GraphicsPort
from .graphics_port_painter import GraphicsPortPainter
from .graphics_scene import GraphicsScene

DefaultGraphicsSceneFactory = providers.Factory(
    GraphicsScene, scene=DefaultSceneFactory
)
