# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, Optional, Set

import dependency_injector.providers as providers
from PySide2.QtCore import QRectF
from PySide2.QtWidgets import QGraphicsItem

from dial_core.node_editor import Port

from .graphics_port_painter import GraphicsPortPainterFactory

if TYPE_CHECKING:
    from .graphics_connection import GraphicsConnection
    from .graphics_node import GraphicsNode
    from PySide2.QtGui import QPainter
    from PySide2.QtCore import QPointF
    from PySide2.QtWidgets import QWidget, QStyleOptionGraphicsItem


class GraphicsPort(QGraphicsItem):
    """Class representing a port for a node.

    Can be used as a start/end point for dragging connections between nodes.

    Attributes:
        graphics_node: Parent GraphicsNode object where this port is located.
        radius: Radius of the port (used for drawing).
        color: Color of the port.
        port: Port object associated with this GraphicsPort object.
        connections: GraphicsConnection objects connected to this port.
    """

    class DrawingState(Enum):
        Normal = 0
        Dragging = 1

    drawing_state = DrawingState.Normal
    drawing_type = None

    def __init__(
        self,
        port: "Port",
        graphics_port_painter_factory,
        parent: "GraphicsNode" = None,
    ):
        super().__init__(parent)

        self.radius = 8
        self.margin = 12

        self.__graphics_node = parent
        self._port = port
        self._port.graphics_port = self  # type: ignore

        self.__graphics_connections: Set["GraphicsConnection"] = set()

        self.__graphics_port_painter_factory = graphics_port_painter_factory
        self.__graphics_port_painter = graphics_port_painter_factory(graphics_port=self)

    @property
    def name(self):  # TODO: Eventually remove
        """Returns the name of the graphics port."""
        return self._port.name

    @property
    def port_type(self):
        return self._port.port_type

    @property
    def graphics_node(self) -> Optional["GraphicsNode"]:
        """Returns the parent GraphicsNode where this port is located."""
        return self.__graphics_node

    @property
    def painter(self):
        return self.__graphics_port_painter

    @property
    def graphics_connections(self) -> Set["GraphicsConnection"]:
        """Returns a list of the GraphicsConnections item connected to this port."""
        return self.__graphics_connections

    def pos(self) -> "QPointF":
        """Returns the position of the GraphicsPort (In terms of scene coordinates)."""
        return (
            self.graphics_node.pos() + super().pos()
            if self.graphics_node
            else super().pos()
        )

    def add_connection(self, connection_item: "GraphicsConnection"):
        """Adds a new GraphicsConnection item to the list of connections.

        Args:
            connection_item: A GraphicsConnection object.
        """

        # If both ports are connected, connect the inner port objects
        if connection_item.start_graphics_port and connection_item.end_graphics_port:
            start_port = connection_item.start_graphics_port._port
            end_port = connection_item.end_graphics_port._port

            if self._port is start_port:
                self._port.connect_to(end_port)
            elif self._port is end_port:
                self._port.connect_to(start_port)
            else:
                #  TODO: Raise exception
                print("This GraphicsConnection object doesn't belong to this port!")

        self.__graphics_connections.add(connection_item)

    def remove_connection(self, connection_item: "GraphicsConnection"):
        """Removes an existent GraphicsConnection item from the list of connections.

        Doesn't do anything if the item to remove is not present on the connections
        list.

        Args:
            connection_item: A GraphicsConnection object.
        """
        self.__graphics_connections.discard(connection_item)

    def boundingRect(self) -> "QRectF":
        """Returns an enclosing rect for the port, PLUS a margin. All the boundingRect()
        area is clickable by the user and can be used as a start/end zone for drag/drop
        connections.

        Important:
            Do not use this function for painting. The area for painting doesn't
            includes the margins, only the radius.
        """
        return QRectF(
            -self.radius - self.margin,
            -self.radius - self.margin,
            2 * self.radius + 2 * self.margin,
            2 * self.radius + 2 * self.margin,
        )

    def __getstate__(self) -> Dict[str, Any]:
        return {"connections": self.__graphics_connections, "pos": self.pos()}

    def __setstate__(self, new_state: Dict[str, Any]):
        self.setPos(new_state["pos"])

    def __reduce__(self):
        return (
            GraphicsPort,
            (self._port, self.__graphics_port_painter_factory, self.__graphics_node),
            self.__getstate__(),
        )

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._port == other._port
        print("asdf")

    def paint(
        self,
        painter: "QPainter",
        option: "QStyleOptionGraphicsItem",
        widget: "QWidget" = None,
    ):
        """Paints the port."""
        self.__graphics_port_painter.paint(painter, option, widget)


GraphicsPortFactory = providers.Factory(
    GraphicsPort, graphics_port_painter_factory=GraphicsPortPainterFactory.delegate()
)
