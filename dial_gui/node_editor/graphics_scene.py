# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import math
from typing import TYPE_CHECKING, List, Tuple

import dependency_injector.providers as providers
from PySide2.QtCore import QLine, QRect
from PySide2.QtGui import QColor, QPen
from PySide2.QtWidgets import QGraphicsScene, QGraphicsItem

from dial_core.node_editor import SceneFactory

from .graphics_node import GraphicsNode, GraphicsNodeFactory

if TYPE_CHECKING:
    from PySide2.QtWidgets import QObject
    from PySide2.QtCore import QRectF
    from dial_core.node_editor import Node, Scene
    from PySide2.QtGui import QPainter
    from .graphics_connection import GraphicsConnection  # noqa: F401


class GraphicsScene(QGraphicsScene):
    def __init__(self, scene: "Scene", parent: "QObject" = None):
        super().__init__(parent)

        self.__scene = scene
        self.__graphics_nodes: List["GraphicsNode"] = []
        self.__graphics_connections: List["GraphicsConnection"] = []

        # Settings
        self.width = 64000
        self.height = 64000

        self.grid_size = 20
        self.grid_squares = 5

        # Colors/Pens/Brushes
        self._color_background = QColor("#393939")
        self._color_light = QColor("#2f2f2f")
        self._color_dark = QColor("#292929")

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)

        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)

        self.setBackgroundBrush(self._color_background)

        self.setSceneRect(
            -self.width // 2, -self.height // 2, self.width, self.height,
        )

        # Populate the graphics scene
        for node in self.__scene:
            graphics_node = self.__create_graphics_node_from(node)
            self.__graphics_nodes.append(graphics_node)
            self.addItem(graphics_node)

    @property
    def scene(self):
        """Returns the scene attached to this graphics scene."""
        return self.__scene

    def addItem(self, item: "QGraphicsItem"):
        if isinstance(item, GraphicsNode):
            self.__add_graphics_node(item)

        elif isinstance(item, GraphicsConnection):
            self.__add_graphics_connection(item)

        super().addItem(item)

    def removeItem(self, item: "QGraphicsItem"):
        if isinstance(item, GraphicsNode):
            self.__remove_graphics_node(item)

        elif isinstance(item, GraphicsConnection):
            self.__remove_graphics_connection(item)

        super().removeItem(item)

    def __add_graphics_node(self, graphics_node: "GraphicsNode"):
        self.__scene.add_node(graphics_node._node)
        self.__graphics_nodes.append(graphics_node)

    def __add_graphics_connection(self, graphics_connection: "GraphicsConnection"):
        self.__graphics_connections.append(graphics_connection)

    def __remove_graphics_node(self, graphics_node: "GraphicsNode"):
        try:
            self.__graphics_nodes.remove(graphics_node)
        except ValueError:
            pass

    def __remove_graphics_connection(self, graphics_connection: "GraphicsConnection"):
        try:
            self.__graphics_connections.remove(graphics_connection)
        except ValueError:
            pass

    def __create_graphics_node_from(self, node: "Node"):
        return GraphicsNodeFactory(node, graphics_scene=self)

    def drawBackground(self, painter: "QPainter", rect: "QRectF"):
        """Draws the background for the scene."""
        super().drawBackground(painter, rect)

        grid_rect = self.__calculate_grid_boundaries(rect)

        # Compute all lines to be drawn
        light_lines, dark_lines = self.__calculate_grid_lines(grid_rect)

        # Draw all lines
        painter.setPen(self._pen_light)
        painter.drawLines(light_lines)

        painter.setPen(self._pen_dark)
        painter.drawLines(dark_lines)

    def __getstate__(self):
        return {
            "scene": self.scene,
            "graphics_nodes": self.__graphics_nodes,
        }

    def __setstate__(self, new_state: dict):
        """Composes a GraphicsScene object from a pickled dict."""
        self.clear()

        self.__scene = new_state["scene"]
        self.__graphics_nodes = new_state["graphics_nodes"]

        for graphics_node in self.__graphics_nodes:
            self.addItem(graphics_node)

            for graphics_port in list(graphics_node.inputs.values()) + list(
                graphics_node.outputs.values()
            ):
                for graphics_connection in graphics_port.graphics_connections:
                    # TODO: Solve items duplication with this approach
                    # self.__graphics_connections.append(graphics_connection)
                    self.addItem(graphics_connection)

        self.update()

    def __reduce__(self):
        # Initialize with an empty scene (Because the real scene will be restored later)
        return (GraphicsScene, ([],), self.__getstate__())

    def __calculate_grid_boundaries(self, rect: "QRectF") -> "QRect":
        """Calculates the grid boundaries from the rect."""
        # Get grid boundaries
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        # Anchor left and top to the closest grid line
        left = left - (left % self.grid_size)
        top = top - (top % self.grid_size)

        return QRect(left, top, right - left + 2, bottom - top + 2)

    def __calculate_grid_lines(self, grid_rect: "QRect") -> Tuple[List, List]:
        """Calculates the coordinates of the horizontal/vertical lines to be drawn.

        Args:
            grid_rect: Rectangle representing the grid boundaries.

        Returns:
            Lists of light lines and dark lines to draw.
        """
        light_lines = []
        dark_lines = []

        # Calculate horizontal lines
        for x in range(grid_rect.left(), grid_rect.right(), self.grid_size):
            if x % (self.grid_size * self.grid_squares) != 0:
                light_lines.append(QLine(x, grid_rect.top(), x, grid_rect.bottom()))
            else:
                dark_lines.append(QLine(x, grid_rect.top(), x, grid_rect.bottom()))

        # Calculate vertical lines
        for y in range(grid_rect.top(), grid_rect.bottom(), self.grid_size):
            if y % (self.grid_size * self.grid_squares) != 0:
                light_lines.append(QLine(grid_rect.left(), y, grid_rect.right(), y))
            else:
                dark_lines.append(QLine(grid_rect.left(), y, grid_rect.right(), y))

        return light_lines, dark_lines


GraphicsSceneFactory = providers.Factory(GraphicsScene, scene=SceneFactory)
