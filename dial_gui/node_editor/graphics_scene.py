# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, List

import dependency_injector.providers as providers
from dial_core.node_editor import Node, Scene, SceneFactory
from dial_core.utils import log
from PySide2.QtWidgets import QGraphicsItem, QGraphicsScene

from .graphics_connection import GraphicsConnection
from .graphics_node import GraphicsNode, GraphicsNodeFactory
from .graphics_scene_painter import GraphicsScenePainterFactory

if TYPE_CHECKING:
    from PySide2.QtWidgets import QObject
    from PySide2.QtCore import QRectF
    from PySide2.QtGui import QPainter

LOGGER = log.get_logger(__name__)


class GraphicsScene(QGraphicsScene):
    def __init__(
        self,
        scene: "Scene",
        painter_factory: "providers.Factory",
        parent: "QObject" = None,
    ):
        super().__init__(parent)

        self.__scene = scene
        self.__graphics_nodes: List["GraphicsNode"] = []

        # Painter
        self._painter_factory = painter_factory
        self._graphics_scene_painter = painter_factory(graphics_scene=self)

        # Populate the graphics scene
        for node in self.__scene:
            graphics_node = self.__create_graphics_node_from(node)
            self.__graphics_nodes.append(graphics_node)
            super().addItem(graphics_node)

    @property
    def scene(self):
        """Returns the scene attached to this graphics scene."""
        return self.__scene

    def addItem(self, item: "QGraphicsItem"):
        if isinstance(item, GraphicsNode):
            self.__add_graphics_node(item)
            return

        super().addItem(item)

    def removeItem(self, item: "QGraphicsItem"):
        if isinstance(item, GraphicsNode):
            self.__remove_graphics_node(item)
            return

        if isinstance(item, GraphicsConnection):
            self.__remove_graphics_connection(item)
            return

        super().removeItem(item)

    def drawBackground(self, painter: "QPainter", rect: "QRectF"):
        """Draws the background for the scene."""
        super().drawBackground(painter, rect)

        self._graphics_scene_painter.drawBackground(painter, rect)

    def __add_graphics_node(self, graphics_node: "GraphicsNode"):
        self.__scene.add_node(graphics_node._node)
        self.__graphics_nodes.append(graphics_node)

        super().addItem(graphics_node)

    def __remove_graphics_node(self, graphics_node: "GraphicsNode"):
        try:
            self.__graphics_nodes.remove(graphics_node)
            self.__scene.remove_node(graphics_node._node)

            for port in list(graphics_node.inputs.values()) + list(
                graphics_node.outputs.values()
            ):
                for connection in port.graphics_connections:
                    self.__remove_graphics_connection(connection)

            super().removeItem(graphics_node)

        except ValueError:
            pass

    def __remove_graphics_connection(self, graphics_connection: "GraphicsConnection"):
        graphics_connection.start_graphics_port = None
        graphics_connection.end_graphics_port = None
        super().removeItem(graphics_connection)

    def __create_graphics_node_from(self, node: "Node"):
        return GraphicsNodeFactory(node, graphics_scene=self)

    def __getstate__(self):
        LOGGER.debug("Saving scene:\n%s", self.__scene)
        return {"scene": self.__scene, "graphics_nodes": self.__graphics_nodes}

    def __setstate__(self, new_state: dict):
        """Composes a GraphicsScene object from a pickled dict."""
        self.clear()

        self.__scene = new_state["scene"]
        self.__graphics_nodes = new_state["graphics_nodes"]

        LOGGER.debug("Loading scene:\n%s", self.__scene)

        for graphics_node in self.__graphics_nodes:
            super().addItem(graphics_node)

            for graphics_port in list(graphics_node.inputs.values()) + list(
                graphics_node.outputs.values()
            ):
                for graphics_connection in graphics_port.graphics_connections:
                    # TODO: Solve items duplication with this approach
                    self.addItem(graphics_connection)

        self.update()

    def __reduce__(self):
        # Return an empty scene (Because the real scene will be restored later)
        return (
            GraphicsScene,
            (Scene(), self._painter_factory,),
            self.__getstate__(),
        )


GraphicsSceneFactory = providers.Factory(
    GraphicsScene,
    scene=SceneFactory,
    painter_factory=GraphicsScenePainterFactory.delegate(),
)
