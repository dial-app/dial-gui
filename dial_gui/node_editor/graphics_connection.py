# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, Any, Optional

import dependency_injector.providers as providers
from PySide2.QtCore import QPointF
from PySide2.QtGui import QPainterPath, QPainterPathStroker
from PySide2.QtWidgets import QGraphicsItem, QGraphicsPathItem

from .graphics_connection_painter import GraphicsConnectionPainterFactory

if TYPE_CHECKING:
    from PySide2.QtGui import QPainter
    from PySide2.QtCore import QRectF
    from PySide2.QtWidgets import QWidget, QStyleOptionGraphicsItem
    from .graphics_port import GraphicsPort
    from .graphics_connection_painter import GraphicsConnectionPainter


class GraphicsConnection(QGraphicsPathItem):
    """Class representing a line between two points (or ports).

    Can be used to drag a connection between two node's ports, for example.

    Attributes:
        color: Color used to draw this connection.
        start: Start point of this connection.
        end: End point of this connection.
        start_graphics_port: GraphicsPort object attached to the start of this
            connection (if any).
        end_graphics_port: GraphicsPort object attached to the end of this
            connection (if any).

    """

    def __init__(
        self, painter_factory: "providers.Factory", parent: "QGraphicsItem" = None,
    ):
        super().__init__(parent)

        # A Connection can be selectable
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.width = 4
        self.clickable_margin = 20

        self.__start = QPointF(0, 0)
        self.__end = QPointF(0, 0)

        self.__start_graphics_port: Optional["GraphicsPort"] = None
        self.__end_graphics_port: Optional["GraphicsPort"] = None

        self._painter_factory = painter_factory
        self._graphics_connection_painter = painter_factory(graphics_connection=self)

        # Draw connections always on bottom
        self.setZValue(-1)

        self._update_path()

    @property
    def painter(self) -> "GraphicsConnectionPainter":
        return self._graphics_connection_painter

    @property
    def start(self) -> "QPointF":
        """Returns the start position coordinate of this connection."""
        return (
            self.__start
            if not self.__start_graphics_port
            else self.__start_graphics_port.pos()
        )

    @start.setter
    def start(self, position: "QPointF"):
        """Sets a new start position coordinate for this connection.

        When a position is set this way, the connection is disconnected from any
        GraphicsPort it may be connected to (Because we're moving the connection away
        from the port)."""
        self.__start = position

        if self.__start_graphics_port:
            self.__start_graphics_port.remove_connection(self)

        self.__start_graphics_port = None

        self._update_path()

    @property
    def end(self) -> "QPointF":
        """Returns the end position of the connection."""
        return (
            self.__end
            if not self.__end_graphics_port
            else self.__end_graphics_port.pos()
        )

    @end.setter
    def end(self, position: "QPointF"):
        """Sets a new end position coordinate for this connection.

        When a position is set this way, the connection is disconnected from any
        GraphicsPort it may be connected to (Because we're moving the connection away
        from the port)."""
        self.__end = position

        if self.__end_graphics_port:
            self.__end_graphics_port.remove_connection(self)

        self.__end_graphics_port = None

        self._update_path()

    @property
    def start_graphics_port(self) -> Optional["GraphicsPort"]:
        """Returns the port connected to the start of this connection."""
        return self.__start_graphics_port

    @start_graphics_port.setter
    def start_graphics_port(self, graphics_port: Optional["GraphicsPort"]):
        """Sets the start of this connection to the `port` position.

        The connection adopts the color of the start port.
        """
        if not graphics_port:
            if self.__start_graphics_port:
                self.__start_graphics_port.remove_connection(self)

            self.start = self.__start
            self.__start_graphics_port = None
        else:
            # Updates the start position
            self.__start = graphics_port.pos()

            # Assigns a new start port
            self.__start_graphics_port = graphics_port
            self.__start_graphics_port.add_connection(self)

            # The connection adopts the color of the port
            self.painter.color = graphics_port.painter.color

        self._update_path()

    @property
    def end_graphics_port(self) -> Optional["GraphicsPort"]:
        """Returns the port connected to the end of this connection."""
        return self.__end_graphics_port

    @end_graphics_port.setter
    # @log_on_end(INFO, "{self} connected to End Port {port}")
    def end_graphics_port(self, graphics_port: "GraphicsPort"):
        """Sets the end of this connection to the `port` position."""
        if not graphics_port:
            if self.__end_graphics_port:
                self.__end_graphics_port.remove_connection(self)

            self.end = self.__end
            self.__end_graphics_port = None
        else:
            # Updates the end position
            self.__end = graphics_port.pos()

            # Assigns a new end port
            self.__end_graphics_port = graphics_port
            self.__end_graphics_port.add_connection(self)

        self._update_path()

    def is_connected(self) -> bool:
        """Returns if the start and end ports are connected."""
        return bool(self.__start_graphics_port and self.__end_graphics_port)

    def _update_path(self):
        """Creates a new bezier path from `self.start` to `self.end`."""
        path = QPainterPath(self.start)

        diffx = self.end.x() - self.start.x()

        c0x = self.start.x() + (diffx / 3)
        c0y = self.start.y()
        c1x = self.end.x() - (diffx / 3)
        c1y = self.end.y()

        path.cubicTo(c0x, c0y, c1x, c1y, self.end.x(), self.end.y())

        self.setPath(path)

    def itemChange(self, change: "QGraphicsItem.GraphicsItemChange", value: Any) -> Any:
        """Checks if any property of the connection has changed.

        In this case, we change the color of the connection when it's selected.
        """
        if change == self.ItemSelectedChange:
            self.painter.highlight_color(value)
            return value

        return super().itemChange(change, value)

    def boundingRect(self) -> "QRectF":
        return self.shape().boundingRect().normalized()

    def shape(self) -> "QPainterPath":
        path_stroker = QPainterPathStroker()
        path_stroker.setWidth(self.width + self.clickable_margin)
        return path_stroker.createStroke(self.path())

    def paint(
        self,
        painter: "QPainter",
        option: "QStyleOptionGraphicsItem",
        widget: "QWidget" = None,
    ):
        """Paints the connection between the start and end points."""

        self._update_path()

        self._graphics_connection_painter.paint(painter, option, widget)

    def __getstate__(self):
        return {
            "start": self.__start,
            "end": self.__end,
            "start_graphics_port": self.__start_graphics_port,
            "end_graphics_port": self.__end_graphics_port,
        }

    def __setstate__(self, new_state: dict):
        self.__start_graphics_port = new_state["start_graphics_port"]
        self.__end_graphics_port = new_state["end_graphics_port"]
        self.__start = new_state["start"]
        self.__end = new_state["end"]

    def __reduce__(self):
        return (GraphicsConnection, (self._painter_factory,), self.__getstate__())

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.start == other.start
            and self.end == other.end
            and self.start_graphics_port == other.start_graphics_port
            and self.end_graphics_port == other.end_graphics_port
        )

    def __str__(self) -> str:
        return (
            f"{type(self).__name__} {self.start} ({self.start_graphics_port})"
            f" {self.end} ({self.end_graphics_port})"
        )


GraphicsConnectionFactory = providers.Factory(
    GraphicsConnection, painter_factory=GraphicsConnectionPainterFactory.delegate(),
)
