# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QColor
from PySide2.QtWidgets import (
    QColorDialog,
    QDialog,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QWidget,
)

if TYPE_CHECKING:
    from PySide2.QtWidgets import QKeyEvent


class TabSettingsDialog(QDialog):
    """The TabSettingsDialog class provides a dialog for picking a new color and name
    for an EditorTabWidget object.

    Attributes:
        name: Current name of the tab.
        Color: Current color of the tab.
    """

    color_changed = Signal(int, QColor)
    name_changed = Signal(int, str)

    def __init__(
        self,
        index=-1,
        name="",
        color=QColor("#FFFFFF"),
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        self.setWindowTitle("Tab settings")

        # Attributes
        self.index = index
        self.__name = name
        self.__color = color

        # Color picker
        self.__color_picker_dialog = QColorDialog(parent)
        self.__color_picker_dialog.setCurrentColor(self.__color)
        self.__color_picker_dialog.currentColorChanged.connect(
            lambda color: self.color_changed.emit(self.index, color)
        )
        self.__color_picker_dialog.finished.connect(self.done)

        # Button for displaying the color picker
        self.__show_color_picker_button = QPushButton(
            "Color...", default=False, autoDefault=False
        )
        self.__show_color_picker_button.clicked.connect(
            lambda: self.__color_picker_dialog.show()
        )

        # Name edit
        self.__name_line_edit = QLineEdit(self.__name, parent=self)
        self.__name_line_edit.setFocus(Qt.PopupFocusReason)
        self.__name_line_edit.textEdited.connect(
            lambda new_text: self.name_changed.emit(self.index, new_text)
        )

        # Configure layout
        self.__main_layout = QHBoxLayout()
        self.__main_layout.addWidget(self.__show_color_picker_button)
        self.__main_layout.addWidget(self.__name_line_edit)
        self.setLayout(self.__main_layout)

    @property
    def name(self) -> "str":
        """Returns the current name of the tab."""
        return self.__name

    @name.setter
    def name(self, name: str):
        """Sets a new name for the tab (programatically).

        Sends a `name_changed` signal.
        """
        self.__name = name
        self.__name_line_edit.setText(self.__name)
        self.name_changed.emit(self.index, self.name)

    @property
    def color(self) -> "QColor":
        """Returns the current color picked for the tab."""
        return self.__color_picker_dialog.currentColor()

    @color.setter
    def color(self, color):
        """Sets a new color for the tab (programatically).

        Sends a `color_changed` signal.
        """
        self.__color_picker_dialog.setCurrentColor(color)

    def accept(self):
        """When the dialog is accepted (Closed saving the changes), send a signal to
        update the text and color."""
        self.name_changed.emit(self.index, self.__name_line_edit.text())
        self.color_changed.emit(
            self.index, self.__color_picker_dialog.currentColor()
        )
        super().accept()

    def keyPressEvent(self, event: "QKeyEvent"):
        """When the Return key is pressed, accept the dialog."""
        if event.key() == Qt.Key_Return:
            self.accept()

        super().keyPressEvent(event)
