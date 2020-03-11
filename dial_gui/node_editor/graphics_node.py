# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, Any, List

import dependency_injector.providers as providers
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QDialog,
    QGraphicsItem,
    QGraphicsObject,
    QGraphicsProxyWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from dial_gui.event_filters import ResizableItemEventFilter

from .graphics_node_painter import GraphicsNodePainterFactory
from .graphics_port import GraphicsPortFactory
from .graphics_port_painter import (
    InputGraphicsPortPainterFactory,
    OutputGraphicsPortPainterFactory,
)

if TYPE_CHECKING:
    from PySide2.QtCore import QRectF
    from PySide2.QtGui import QPainter, QMouseEvent

    from dial_core.node_editor import Node
    from PySide2.QtWidgets import QStyleOptionGraphicsItem, QGraphicsSceneMouseEvent
    from dial_gui.node_editor import GraphicsPort  # noqa: F401


class GraphicsNode(QGraphicsObject):
    def __init__(
        self,
        node: "Node",
        painter_factory: "providers.Factory",
        parent: "QGraphicsItem" = None,
    ):
        super().__init__(parent)

        # Components
        self._node = node
        self._node.graphics_node = self  # type: ignore

        # GraphicsPorts
        self._input_graphics_ports: List["GraphicsPort"] = []
        self._output_graphics_ports: List["GraphicsPort"] = []
        self.__create_graphic_ports()

        # Proxy
        self._node_widget_proxy = QGraphicsProxyWidget(parent=self)
        self._node_widget_proxy.setWidget(
            self._node.inner_widget if self._node.inner_widget else QWidget()
        )

        # Painter
        self._painter_factory = painter_factory
        self._graphics_node_painter = painter_factory(graphics_node=self)

        # Flags
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)

        # Filters
        self.__resizable_item_event_filter = ResizableItemEventFilter(parent=self)
        self.installEventFilter(self.__resizable_item_event_filter)

    @property
    def title(self):
        return self._node.title

    @property
    def proxy_widget(self) -> "QGraphicsProxyWidget":
        """Returns the widget used for containing the inner widget."""
        return self._node_widget_proxy

    @property
    def painter(self):
        return self._graphics_node_painter

    def __create_graphic_ports(self):
        """Creates new GraphicsPort items from regular Port objects."""

        def create_graphics_ports_from(ports_list, painter_factory):
            return [
                GraphicsPortFactory(port, painter_factory=painter_factory, parent=self)
                for port in ports_list
            ]

        self._input_graphics_ports = create_graphics_ports_from(
            self._node.inputs.values(), InputGraphicsPortPainterFactory
        )

        self._output_graphics_ports = create_graphics_ports_from(
            self._node.outputs.values(), OutputGraphicsPortPainterFactory
        )

    def setInnerWidget(self, widget: "QWidget"):
        """Sets a new widget inside the node."""
        self.prepareGeometryChange()

        self._node_widget_proxy.setWidget(widget)

        self._graphics_node_painter.repositionWidget()
        self._graphics_node_painter.recalculateGeometry()

    def boundingRect(self) -> "QRectF":
        """Returns a rect enclosing the node."""
        return self._graphics_node_painter.boundingRect()

    def itemChange(self, change: "QGraphicsItem.GraphicsItemChange", value: Any) -> Any:
        if change == self.ItemSelectedChange:
            self._graphics_node_painter.itemChange(change, value)

            # Selected items gets a high Z value, so they're displayed on top of other
            # nodes. When unselected, return back to a low Z value.
            if value:
                self.setZValue(10)
            else:
                self.setZValue(0)

            return value

        return super().itemChange(change, value)

    def mouseDoubleClickEvent(self, event: "QGraphicsSceneMouseEvent"):
        if event.button() == Qt.LeftButton:
            self.__toggle_widget_dialog(event)

    def __toggle_widget_dialog(self, event: "QMouseEvent"):
        """Shows the Node `inner_widget` on a new dialog. The content of the node is
        substituted with a button that hides the dialog and shows the inner_widget back
        in the node when pressed.
        """

        node_inner_widget = self.proxy_widget.widget()
        previous_node_size = node_inner_widget.size()

        show_here_button = QPushButton("Show here")
        show_here_button.setMinimumSize(200, 100)

        # Replace the node widget with the button
        self.setInnerWidget(show_here_button)

        # Create a new dialog for displaying the node widget
        dialog = QDialog()
        dialog.setWindowTitle(self._node.title)

        layout = QVBoxLayout()
        layout.addWidget(node_inner_widget)
        dialog.setLayout(layout)

        dialog.show()

        def place_widget_back_in_node():
            # Widgets embedded in nodes can't have parents
            node_inner_widget.setParent(None)

            node_inner_widget.resize(previous_node_size)
            self.setInnerWidget(node_inner_widget)

            dialog.close()

        # The widget will be displayed back in the node when the dialog is closed or
        # when the "show here" button is pressed
        dialog.finished.connect(place_widget_back_in_node)
        show_here_button.clicked.connect(place_widget_back_in_node)

    def __setstate__(self, new_state: dict):
        self.prepareGeometryChange()

        self.setPos(new_state["pos"])

        self._node_widget_proxy.resize(500, 200)

        print("Current inputs", self._input_graphics_ports)
        print("Current outputs", self._output_graphics_ports)
        print("Old inputs", new_state["inputs"])
        print("Old outputs", new_state["outputs"])

    def __reduce__(self):
        return (
            GraphicsNode,
            (self._node, None),
            {
                "pos": self.pos(),
                "proxy_geometry": self._node_widget_proxy.geometry(),
                "inputs": self._input_graphics_ports,
                "outputs": self._output_graphics_ports,
            },
        )

    def paint(
        self, painter: "QPainter", option: "QStyleOptionGraphicsItem", widget: "QWidget"
    ):
        """Paints the GraphicsNode item."""

        self._graphics_node_painter.paint(painter, option, widget)


GraphicsNodeFactory = providers.Factory(
    GraphicsNode, painter_factory=GraphicsNodePainterFactory.delegate()
)
