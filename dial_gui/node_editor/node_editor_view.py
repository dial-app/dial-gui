# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, Any, Optional, Union

from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QGraphicsItem, QGraphicsView

from dial_core.utils import log
from dial_gui.event_filters import PanningEventFilter, ZoomEventFilter
from dial_gui.node_editor import GraphicsConnectionFactory, GraphicsPort

if TYPE_CHECKING:
    from PySide2.QtCore import QObject
    from PySide2.QtGui import QMouseEvent, QWheelEvent
    from PySide2.QtWidgets import QTabWidget, QWidget
    from dial_gui.node_editor import GraphicsConnection


class NodeEditorView(QGraphicsView):
    connection_created = Signal(QGraphicsItem)
    connection_removed = Signal(QGraphicsItem)

    def __init__(self, tabs_widget: "QTabWidget", parent: "QWidget" = None):
        super().__init__(parent)

        self.__tabs_widget = tabs_widget

        self.__new_connection: Optional["GraphicsConnection"] = None

        self.__panning_event_filter = PanningEventFilter(parent=self)
        self.__zoom_event_filter = ZoomEventFilter(parent=self)
        self.installEventFilter(self.__zoom_event_filter)

        self.setRenderHints(
            QPainter.Antialiasing
            | QPainter.HighQualityAntialiasing
            | QPainter.TextAntialiasing
            | QPainter.SmoothPixmapTransform
        )

        self.setDragMode(QGraphicsView.RubberBandDrag)

        # View actions
        self.set_panning(True)
        self.set_zooming(True)

        # Hide scrollbars
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Set anchor under mouse (for zooming)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    def set_panning(self, toggle: bool):
        """Toggles if the view can be panned or not with the mouse."""
        self.__toggle_event_filter(toggle, self.__panning_event_filter)

    def set_zooming(self, toggle: bool):
        """Toggles if the view can be zoomed or not with the mouse wheel."""
        self.__toggle_event_filter(toggle, self.__zoom_event_filter)

    def mousePressEvent(self, event: "QMouseEvent"):
        # TODO: Explain why
        # event.ignore()
        if event.button() == self.__panning_event_filter.button_used_for_panning:
            event.ignore()
            return

        if event.button() == Qt.LeftButton:
            self.__start_dragging_connection(event)
            return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: "QMouseEvent"):
        # TODO: Explain why
        # event.ignore()
        if self.__panning_event_filter.is_panning():
            event.ignore()
            return

        if self.__is_dragging_connection():
            self.__dragging_connection(event)
            return

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: "QMouseEvent"):
        # TODO: Explain why
        if self.__panning_event_filter.is_panning():
            event.ignore()
            return

        if event.button() == Qt.LeftButton:
            self.__stop_dragging_connection(event)

        super().mouseReleaseEvent(event)

    def wheelEvent(self, event: "QWheelEvent"):
        # TODO: Explain why
        event.ignore()

    def __start_dragging_connection(self, event: "QMouseEvent"):
        """Starts creating a new connection by dragging the mouse.

        Only works when the user clicks on a GraphicsPort item.

        Args:
            event: Mouse event.
        """
        item: "GraphicsPort" = self.__item_clicked_on(event)

        if not isinstance(item, GraphicsPort):
            super().mousePressEvent(event)
            return

        log.get_logger(__name__).debug("Start dragging")

        self.__new_connection = self.__create_new_connection()
        self.__new_connection.start_graphics_port = item
        self.__new_connection.end = self.mapToScene(event.pos())

        # Its important to don't pass the event to parent classes to avoid selecting
        # items when we start dragging.
        # DON'T include `super().mousePressEvent(event)` here

    def __stop_dragging_connection(self, event: "QMouseEvent"):
        """Stops dragging the connection.

        If the connection doesn't end on a GraphicsPort, the connection item is removed
        from the scene.

        Args:
            event: Mouse event.
        """
        if not self.__is_dragging_connection() or not self.__new_connection:
            super().mouseReleaseEvent(event)
            return

        item = self.__item_clicked_on(event)

        # The conection must end on a COMPATIBLE GraphicsPort item
        if isinstance(item, GraphicsPort) and item.is_compatible_with(
            self.__new_connection.start_graphics_port  # type: ignore
        ):
            self.__new_connection.end_graphics_port = item
        else:
            self.__remove_connection(self.__new_connection)

        # Reset the connection item
        self.__new_connection = None

        super().mouseReleaseEvent(event)

    def __dragging_connection(self, event: "QMouseEvent"):
        """Drags a connection while the mouse is moving.

        Args:
            event: Mouse event.
        """
        if not self.__new_connection:
            super().mouseMoveEvent(event)
            return

        self.__new_connection.end = self.mapToScene(event.pos())

        item = self.__item_clicked_on(event)
        if isinstance(item, GraphicsPort):
            self.__new_connection.end = item.pos()

        super().mouseMoveEvent(event)

    def __is_dragging_connection(self) -> bool:
        """Checks if the user is currently dragging a connection or not."""
        return self.__new_connection is not None

    def __item_clicked_on(self, event: "QMouseEvent") -> Union["GraphicsPort", Any]:
        """Returns the graphical item under the mouse."""
        return self.itemAt(event.pos())

    def __create_new_connection(self) -> "GraphicsConnection":
        """Create a new connection on the scene."""
        connection = GraphicsConnectionFactory()

        self.connection_created.emit(connection)

        return connection

    def __remove_new_connection(self, connection: "GraphicsConnection"):
        """Removes the GraphicsConnection item from the scene."""
        connection.start_graphics_port = None
        connection.end_graphics_port = None

        self.connection_removed.emit(connection)

        return connection

    def __toggle_event_filter(self, toggle: bool, event_filter: "QObject"):
        """Toggles (Installs/Uninstalls) the specified event filter on this object."""
        if toggle:
            self.installEventFilter(event_filter)
        else:
            self.uninstallEventFilter(event_filter)
