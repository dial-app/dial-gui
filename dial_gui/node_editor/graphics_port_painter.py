# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import Enum
from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from PySide2.QtCore import QRectF, Qt
from PySide2.QtGui import QBrush, QPainter, QPen
from PySide2.QtWidgets import QGraphicsItem, QGraphicsTextItem

from .type_colors import TypeColor

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget, QStyleOptionGraphicsItem
    from .graphics_port import GraphicsPort


class GraphicsPortPainter:
    """The GraphicsPortPainter class provides a set of functions and configurations for
        painting a GraphicsPort object.
    """

    class DrawingState(Enum):
        Normal = 0
        Target = 1

    class PortNamePosition(Enum):
        Left = 0
        Right = 1

    drawing_state = DrawingState.Normal
    target_port_type = None

    def __init__(
        self, graphics_port: "GraphicsPort", port_name_position: "PortNamePosition"
    ):
        self.__graphics_port = graphics_port
        self.__port_name = QGraphicsTextItem(parent=graphics_port)
        self.__port_name.setPlainText(graphics_port._port.name)
        self.__port_name.setDefaultTextColor("#FFFFFF")
        self.__port_name.setFlag(QGraphicsItem.ItemStacksBehindParent)

        self.port_name_position = port_name_position

        # Colors/Pens/Brushes

        self.__color = TypeColor.get_color_for(graphics_port._port.port_type)

        self.__outline_pen = QPen(self.__color.darker())
        self.__outline_pen.setWidthF(2)
        self.__background_brush = QBrush(self.__color)

        self.__dashed_outline_pen = QPen(self.__color)
        self.__dashed_outline_pen.setStyle(Qt.DashLine)
        self.__dashed_outline_pen.setWidth(2)

    @property
    def port_name_position(self) -> "PortNamePosition":
        return self.__port_name_position

    @port_name_position.setter
    def port_name_position(self, position: "PortNamePosition"):
        if position == self.PortNamePosition.Left:
            self.__port_name.setPos(-self.__port_name.boundingRect().width() - 3, 1)
        elif position == self.PortNamePosition.Right:
            self.__port_name.setPos(3, 1)

        self.__port_name_position = position

    @property
    def color(self):
        return self.__color

    def paint_area(self):
        return QRectF(
            -self.__graphics_port.radius,
            -self.__graphics_port.radius,
            2 * self.__graphics_port.radius,
            2 * self.__graphics_port.radius,
        )

    def paint(
        self,
        painter: "QPainter",
        option: "QStyleOptionGraphicsItem",
        widget: "QWidget" = None,
    ):
        if (
            GraphicsPortPainter.drawing_state == GraphicsPortPainter.DrawingState.Target
            and self.__graphics_port.port_type == GraphicsPortPainter.target_port_type
        ):
            painter.setPen(self.__dashed_outline_pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(self.__graphics_port.boundingRect())

        painter.setPen(self.__outline_pen)
        painter.setBrush(self.__background_brush)
        painter.drawEllipse(self.paint_area())


GraphicsPortPainterFactory = providers.Factory(
    GraphicsPortPainter, port_name_position=GraphicsPortPainter.PortNamePosition.Left
)

InputGraphicsPortPainterFactory = providers.Factory(
    GraphicsPortPainter, port_name_position=GraphicsPortPainter.PortNamePosition.Left
)

OutputGraphicsPortPainterFactory = providers.Factory(
    GraphicsPortPainter, port_name_position=GraphicsPortPainter.PortNamePosition.Right
)
