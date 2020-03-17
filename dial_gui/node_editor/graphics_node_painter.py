# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, Any

import dependency_injector.providers as providers
from PySide2.QtCore import QRectF, Qt
from PySide2.QtGui import QBrush, QColor, QPainter, QPainterPath, QPen
from PySide2.QtWidgets import QGraphicsItem, QGraphicsTextItem

if TYPE_CHECKING:
    from .graphics_node import GraphicsNode
    from PySide2.QtWidgets import QStyleOptionGraphicsItem, QWidget


class GraphicsNodePainter:
    def __init__(self, graphics_node: "GraphicsNode"):
        self.__graphics_node = graphics_node

        # Dimensions
        self.padding = 12
        self.clickable_margin = 15
        self.round_edge_size = 10

        # Colors/Pens/Brushes
        self.__title_color = Qt.white
        self.__outline_selected_color = QColor("#FFA637")
        self.__outline_default_color = QColor("#000000")

        self.__outline_pen = QPen(self.__outline_default_color)
        self.__title_background_brush = QBrush(QColor("#FF313131"))
        self.__background_brush = QBrush(QColor("#E3212121"))

        # Graphics Components
        self.__graphics_title = QGraphicsTextItem(parent=graphics_node)
        self.__graphics_title.setDefaultTextColor(self.__title_color)
        self.__graphics_title.setPlainText(self.__graphics_node.title)
        self.__graphics_title.setPos(self.padding, 0)

        # Position ProxyWidget
        self.repositionWidget()

        # position GraphicsPort objects
        def position_graphics_ports(x_offset, graphics_ports_dict):
            for i, graphics_port in enumerate(graphics_ports_dict.values()):
                graphics_port.setPos(
                    x_offset, self.title_height() + (graphics_port.radius * 4) * (i + 1)
                )

        position_graphics_ports(0, self.__graphics_node.inputs)
        position_graphics_ports(
            self.boundingRect().width(), self.__graphics_node.outputs
        )

    @property
    def outline_selected_color(self) -> "QColor":
        return self.__outline_selected_color

    @outline_selected_color.setter
    def outline_selected_color(self, color: "QColor"):
        self.__outline_selected_color = color

    @property
    def outline_default_color(self) -> "QColor":
        return self.__outline_default_color

    @outline_default_color.setter
    def outline_default_color(self, color: "QColor"):
        self.__outline_default_color = color

    def boundingRect(self) -> "QRectF":
        proxy_rect = self.__graphics_node._proxy_widget.boundingRect()

        return proxy_rect.adjusted(
            0, 0, self.padding * 2, self.title_height() + self.padding * 2
        ).normalized()

    def repositionWidget(self):
        self.__graphics_node._proxy_widget.setPos(
            self.padding, self.title_height() + self.padding
        )

    def recalculateGeometry(self):
        for graphics_port in self.__graphics_node.outputs.values():
            graphics_port.setX(self.boundingRect().width())

    def itemChange(self, change: "QGraphicsItem.GraphicsItemChange", value: Any) -> Any:
        if change == QGraphicsItem.ItemSelectedChange:
            self.__outline_pen.setColor(
                self.__outline_selected_color if value else self.__outline_default_color
            )

        return value

    def title_height(self) -> int:
        """Returns the height of the title graphics item."""
        return self.__graphics_title.boundingRect().height()

    def paint(
        self, painter: "QPainter", option: "QStyleOptionGraphicsItem", widget: "QWidget"
    ):
        """Paints the GraphicsNode item."""

        self.__paint_background(painter)
        self.__paint_title_background(painter)
        self.__paint_outline(painter)

    def __paint_background(self, painter: "QPainter"):
        """Paints the background of the node. Plain color, no lines."""
        path_background = QPainterPath()
        path_background.addRoundedRect(
            self.__graphics_node.boundingRect(),
            self.round_edge_size,
            self.round_edge_size,
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(self.__background_brush)

        painter.drawPath(path_background.simplified())

    def __paint_title_background(self, painter: "QPainter"):
        """Paints a little background behind the title text, at the top of the node."""
        title_rect = self.__graphics_title.boundingRect()

        path_title_background = QPainterPath()
        path_title_background.setFillRule(Qt.WindingFill)
        path_title_background.addRoundedRect(
            0,
            0,
            self.__graphics_node.boundingRect().width(),
            title_rect.height(),
            self.round_edge_size,
            self.round_edge_size,
        )

        # (Drawing rects to hide the two botton round edges)
        path_title_background.addRect(
            0,
            title_rect.height() - self.round_edge_size,
            self.round_edge_size,
            self.round_edge_size,
        )

        path_title_background.addRect(
            self.__graphics_node.boundingRect().width() - self.round_edge_size,
            title_rect.height() - self.round_edge_size,
            self.round_edge_size,
            self.round_edge_size,
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(self.__title_background_brush)
        painter.drawPath(path_title_background.simplified())

    def __paint_outline(self, painter: "QPainter"):
        """Paints the outline of the node. Depending on if its selected or not, the
        color of the outline changes."""
        path_outline = QPainterPath()
        path_outline.addRoundedRect(
            self.__graphics_node.boundingRect(),
            self.round_edge_size,
            self.round_edge_size,
        )

        painter.setPen(self.__outline_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())


GraphicsNodePainterFactory = providers.Factory(GraphicsNodePainter)
