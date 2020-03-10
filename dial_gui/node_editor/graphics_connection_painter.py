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
        self.__color = QColor("black")

        self.__default_pen = QPen(self.__color)
        self.__default_pen.setWidth(self.__graphics_connection.width)

    @property
    def color(self) -> "QColor":
        """Returns the color of this connection."""
        return self.__color

    @color.setter
    def color(self, color: "QColor"):
        """Sets a new color for the connection, updating the QPen used for painting."""
        self.__color = color
        self.__default_pen.setColor(self.__color)

    def paint(
        self,
        painter: "QPainter",
        option: "QStyleOptionGraphicsItem",
        widget: "QWidget" = None,
    ):
        painter.setPen(self.__default_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.__graphics_connection.path())


GraphicsConnectionPainterFactory = providers.Factory(GraphicsConnectionPainter)
