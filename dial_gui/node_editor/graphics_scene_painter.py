# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import math
from typing import TYPE_CHECKING, List, Tuple

import dependency_injector.providers as providers
from PySide2.QtCore import QLine, QRect, QRectF
from PySide2.QtGui import QColor, QPainter, QPen

if TYPE_CHECKING:
    from .graphics_scene import GraphicsScene


class GraphicsScenePainter:
    def __init__(self, graphics_scene: "GraphicsScene"):
        self.__graphics_scene = graphics_scene

        self.width = 64000
        self.height = 64000

        self.__graphics_scene.setSceneRect(
            -self.width // 2, -self.height // 2, self.width, self.height,
        )

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

        self.__graphics_scene.setBackgroundBrush(self._color_background)

    def drawBackground(self, painter: "QPainter", rect: "QRectF"):
        grid_rect = self.__calculate_grid_boundaries(rect)

        # Compute all lines to be drawn
        light_lines, dark_lines = self.__calculate_grid_lines(grid_rect)

        # Draw all lines
        painter.setPen(self._pen_light)
        painter.drawLines(light_lines)

        painter.setPen(self._pen_dark)
        painter.drawLines(dark_lines)

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


GraphicsScenePainterFactory = providers.Factory(GraphicsScenePainter)
