# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, Any, Dict

import dependency_injector.providers as providers
from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import (
    QDialog,
    QGraphicsItem,
    QGraphicsObject,
    QGraphicsProxyWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from dial_gui.event_filters import ResizableNodeEventFilter

from .graphics_node_painter import GraphicsNodePainterFactory
from .graphics_port import GraphicsPortFactory
from .graphics_port_painter import (
    InputGraphicsPortPainterFactory,
    OutputGraphicsPortPainterFactory,
)

if TYPE_CHECKING:
    from PySide2.QtCore import QRectF
    from PySide2.QtGui import QPainter, QMouseEvent

    from dial_core.node_editor import Node, Port  # noqa: F401
    from PySide2.QtWidgets import QStyleOptionGraphicsItem, QGraphicsSceneMouseEvent
    from dial_gui.node_editor import GraphicsPort  # noqa: F401
    from .graphics_scene import GraphicsScene


class GraphicsNode(QGraphicsObject):
    class ProxyWidget(QGraphicsProxyWidget):
        widget_resized = Signal("QSizeF")

        def resize(self, x_or_point, y=None):
            if isinstance(x_or_point, float):
                super().resize(x_or_point, y)
            else:
                super().resize(x_or_point)

            self.widget_resized.emit(self.size())

    def __init__(
        self,
        node: "Node",
        painter_factory: "providers.Factory",
        graphics_scene: "GraphicsScene" = None,
        parent: "QGraphicsItem" = None,
    ):
        super().__init__(parent)

        # Components
        self._node = node
        self._node.graphics_node = self  # type: ignore
        self.__graphics_scene = graphics_scene

        # GraphicsPorts
        self._input_graphics_ports = self.__create_graphics_ports(
            self._node.inputs, InputGraphicsPortPainterFactory
        )
        self._output_graphics_ports = self.__create_graphics_ports(
            self._node.outputs, OutputGraphicsPortPainterFactory
        )
        # Proxy
        self._proxy_widget = self.ProxyWidget(parent=self)
        self._proxy_widget.setWidget(
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
        self.__resizable_node_event_filter = ResizableNodeEventFilter(parent=self)
        self.installEventFilter(self.__resizable_node_event_filter)

        # Connections
        self._proxy_widget.widget_resized.connect(
            lambda _: self._graphics_node_painter.recalculateGeometry()
        )

    @property
    def title(self):
        return self._node.title

    @property
    def painter(self):
        return self._graphics_node_painter

    @property
    def inputs(self):
        return self._input_graphics_ports

    @property
    def outputs(self):
        return self._output_graphics_ports

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

        node_inner_widget = self._proxy_widget.widget()
        previous_node_size = node_inner_widget.size()

        show_here_button = QPushButton("Show here")
        show_here_button.setMinimumSize(200, 100)

        # Replace the node widget with the button
        self.__set_inner_widget(show_here_button)

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
            self.__set_inner_widget(node_inner_widget)

            dialog.close()

        # The widget will be displayed back in the node when the dialog is closed or
        # when the "show here" button is pressed
        dialog.finished.connect(place_widget_back_in_node)
        show_here_button.clicked.connect(place_widget_back_in_node)

    def __set_inner_widget(self, widget: "QWidget"):
        """Sets a new widget inside the node."""
        self.prepareGeometryChange()

        self._proxy_widget.setWidget(widget)

        self._graphics_node_painter.repositionWidget()
        self._graphics_node_painter.recalculateGeometry()

    def __create_graphics_ports(
        self, ports_dict: Dict[str, "Port"], painter_factory: "providers.Factory"
    ) -> Dict[str, "GraphicsPort"]:
        """Creates new GraphicsPort items from regular Port objects."""
        graphics_ports_dict = {}

        for name in ports_dict.keys():
            port = ports_dict[name]

            try:
                port.graphics_port.painter_factory = painter_factory
                port.graphics_port.set_parent_graphics_node(self)
                graphics_ports_dict[name] = port.graphics_port

            except AttributeError:
                graphics_ports_dict[name] = GraphicsPortFactory(
                    port=port, painter_factory=painter_factory, parent=self
                )

        return graphics_ports_dict

    def __getstate__(self):
        return {"pos": self.pos(), "proxy_size": self._proxy_widget.size()}

    def __setstate__(self, new_state: dict):
        self.prepareGeometryChange()
        self.setPos(new_state["pos"])

        self._proxy_widget.resize(new_state["proxy_size"])

    def __reduce__(self):
        return (GraphicsNode, (self._node, self._painter_factory), self.__getstate__())

    def paint(
        self, painter: "QPainter", option: "QStyleOptionGraphicsItem", widget: "QWidget"
    ):
        """Paints the GraphicsNode item."""
        self._graphics_node_painter.paint(painter, option, widget)


GraphicsNodeFactory = providers.Factory(
    GraphicsNode, painter_factory=GraphicsNodePainterFactory.delegate()
)
