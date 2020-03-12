# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import Enum, Flag, auto
from typing import TYPE_CHECKING

from PySide2.QtCore import QEvent, QObject, Qt

if TYPE_CHECKING:
    from dial_gui.widget_editor import Graphicswidget


class ResizableItemEventFilter(QObject):
    """The ResizableItemEventFilter class provides resizing anchors for a Graphicswidget
    object.

    The anchors can be dragged freely using the mouse, and the widget will be resized
    accordingly.

    Important:
        This filter only works with a Graphicswidget object.

    Attributes:
        resize_margins: Size of the margins that can be clicked to start the resizing
        event.
        button_used_for_resizing: The button that mast be pressed and dragged for
        resizing the widget.

    Examples:
        widget = Graphicswidget()
        resizable_widget_event_filter = ResizablewidgetEventFilter()

        widget.installEventFilter(resizable_widget_event_filter)
    """

    class State(Enum):
        Idle = 0
        Resizing = 1

    class MarginClicked(Flag):
        NoMargin = 0
        Top = auto()
        Bottom = auto()
        Left = auto()
        Right = auto()

    def __init__(self, parent: "QObject" = None):
        super().__init__(parent)

        self.__state = self.State.Idle
        self.__margins_clicked = self.MarginClicked.NoMargin

        self.resize_margins = 12

        self.button_used_for_resizing = Qt.LeftButton

    @property
    def state(self) -> "ResizableItemEventFilter.State":
        """Returns the state of the event filter (Normal, Resizing...)"""
        return self.__state

    def is_resizing(self) -> bool:
        """Checks if the event filter is currently resizing an object."""
        return self.__state == self.State.Resizing

    def eventFilter(self, widget: "QObject", event: "QEvent") -> bool:
        """Tracks the mouse movements to do the actual resizing.

        When the mouse hovers over the widget, the cursor icon is changed to reflect the
        direction of the resizing (P.E: If the mouse is on the left side of the widget,
        a <-> icon will appear).

        When the resizing button is clicked, the widget will be resized until the button
        is released.
        """
        if event.type() == QEvent.GraphicsSceneHoverMove:
            self.__track_margins_under_cursor(widget, event)
            return True

        if self.__resize_button_clicked(event) and self.__is_inside_resize_margins(
            widget, event
        ):
            self.__start_resizing_widget(widget, event)
            return True

        if self.is_resizing():
            if event.type() == QEvent.GraphicsSceneMouseMove:
                self.__resizing_widget(widget, event)
                return True

            if self.__resize_button_released(event):
                self.__stop_resizing_widget(widget, event)
                return True

        return super().eventFilter(widget, event)

    def __resize_button_clicked(self, event: "QEvent") -> bool:
        """Checks if the button designed for resizing was pressed."""
        return (
            event.type() == QEvent.GraphicsSceneMousePress
            and event.button() == self.button_used_for_resizing
        )

    def __resize_button_released(self, event: "QEvent") -> bool:
        """Checks if the button designed for resizing was released."""
        return (
            event.type() == QEvent.GraphicsSceneMouseRelease
            and event.button() == self.button_used_for_resizing
        )

    def __start_resizing_widget(self, widget: "Graphicswidget", event: "QEvent"):
        """Starts resizing the widget.

        Saves some positions for reference during the resizing event.
        """
        self.__state = self.State.Resizing

        # Saves some information of the cursor and the widget prior to resizing
        self.__initial_resize_pos = event.scenePos()
        self.__initial_widget_pos = widget.pos()
        self.__initial_widget_size = widget.size()

    def __resizing_widget(self, widget: "Graphicswidget", event: "QEvent"):
        """Resizes the widget while dragging one of the margins. Calculates the resulting
        size and position of the widget and applies it."""
        diff = event.scenePos() - self.__initial_resize_pos

        new_x = 0
        new_y = 0
        new_w = 0
        new_h = 0

        if self.__margins_clicked & self.MarginClicked.Left:
            new_x = (
                diff.x()
                if widget.size().width() > widget.minimumSize().width()
                else self.__initial_widget_size.width() - widget.minimumSize().width()
            )
            new_w = -diff.x()

        elif self.__margins_clicked & self.MarginClicked.Right:
            new_w = diff.x()

        if self.__margins_clicked & self.MarginClicked.Top:
            new_y = (
                diff.y()
                if widget.size().height() > widget.minimumSize().height()
                else self.__initial_widget_size.height() - widget.minimumSize().height()
            )
            new_h = -diff.y()

        elif self.__margins_clicked & self.MarginClicked.Bottom:
            new_h = diff.y()

        widget.prepareGeometryChange()

        widget.resize(
            self.__initial_widget_size.width() + new_w,
            self.__initial_widget_size.height() + new_h,
        )

        widget.setPos(
            self.__initial_widget_pos.x() + new_x, self.__initial_widget_pos.y() + new_y
        )

        # widget.recalculateGeometry()

    def __stop_resizing_widget(self, widget: "Graphicswidget", event: "QEvent"):
        """Stops resizing the widget."""
        self.__state = self.State.Idle

    def __is_inside_resize_margins(
        self, widget: "Graphicswidget", event: "QEvent"
    ) -> bool:
        """Checks if the cursor is currently on the margins of the widget."""
        return self.__margins_clicked != self.MarginClicked.NoMargin

    def __track_margins_under_cursor(self, widget: "Graphicswidget", event: "QEvent"):
        """Sets different flags marking on top of which margin the cursor is."""
        x_pos = event.pos().x()
        y_pos = event.pos().y()

        # Horizontal margins
        if x_pos <= self.resize_margins:
            self.__margins_clicked |= self.MarginClicked.Left
            widget.setCursor(Qt.SizeHorCursor)
        elif widget.boundingRect().width() - x_pos <= self.resize_margins:
            self.__margins_clicked |= self.MarginClicked.Right
            widget.setCursor(Qt.SizeHorCursor)
        else:
            self.__margins_clicked &= ~self.MarginClicked.Left
            self.__margins_clicked &= ~self.MarginClicked.Right

        # Vertical margins
        if y_pos <= self.resize_margins:
            self.__margins_clicked |= self.MarginClicked.Top
            widget.setCursor(Qt.SizeVerCursor)
        elif widget.boundingRect().height() - y_pos <= self.resize_margins:
            self.__margins_clicked |= self.MarginClicked.Bottom
            widget.setCursor(Qt.SizeVerCursor)
        else:
            self.__margins_clicked &= ~self.MarginClicked.Top
            self.__margins_clicked &= ~self.MarginClicked.Bottom

        if self.__margins_clicked == (self.MarginClicked.Left | self.MarginClicked.Top):
            widget.setCursor(Qt.SizeFDiagCursor)

        if self.__margins_clicked == (
            self.MarginClicked.Left | self.MarginClicked.Bottom
        ):
            widget.setCursor(Qt.SizeBDiagCursor)

        if self.__margins_clicked == (
            self.MarginClicked.Right | self.MarginClicked.Top
        ):
            widget.setCursor(Qt.SizeBDiagCursor)

        if self.__margins_clicked == (
            self.MarginClicked.Right | self.MarginClicked.Bottom
        ):
            widget.setCursor(Qt.SizeFDiagCursor)

        if self.__margins_clicked == self.MarginClicked.NoMargin:
            widget.unsetCursor()
