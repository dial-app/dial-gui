# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from PySide2.QtCore import Qt
from PySide2.QtGui import QColor, QPen

if TYPE_CHECKING:
    from .graphics_connection import GraphicsConnection
    from PySide2.QtGui import QPainter
    from PySide2.QtWidgets import QWidget, QStyleOptionGraphicsItem


class GraphicsConnectionPainter:
    def __init__(self, graphics_connection: "GraphicsConnection"):

        self.__graphics_connection = graphics_connection

        # Colors/Pens/Brushes
        self._color = QColor("black")

        self._default_pen = QPen(self._color)
        self._default_pen.setWidth(self.__graphics_connection.width)

    @property
    def color(self) -> "QColor":
        """Returns the color of this connection."""
        return self._color

    @color.setter
    def color(self, color: "QColor"):
        """Sets a new color for the connection, updating the QPen used for painting."""
        self._color = color
        self._default_pen.setColor(self._color)

    def highlight_color(self, toggle: bool):
        """Paints the connection with a highlighted color if toggled."""
        self._default_pen.setColor(self._color.lighter(150) if toggle else self._color)

    def paint(
        self,
        painter: "QPainter",
        option: "QStyleOptionGraphicsItem",
        widget: "QWidget" = None,
    ):
        """Paints the graphics connection item."""
        painter.setPen(self._default_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.__graphics_connection.path())


GraphicsConnectionPainterFactory = providers.Factory(GraphicsConnectionPainter)
