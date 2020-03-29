# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import Signal
from PySide2.QtGui import QColor
from PySide2.QtWidgets import (
    QColorDialog,
    QDialog,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QWidget,
)


class TabSettingsDialog(QDialog):
    current_color_changed = Signal(int, QColor)
    current_name_changed = Signal(int, str)

    def __init__(
        self,
        index=-1,
        name="",
        current_color=QColor("#FFFFFF"),
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        self.setWindowTitle("Tab settings")

        self.index = index
        self.__name = name
        self.__current_color = current_color

        self.__color_picker_dialog = QColorDialog(parent=self)
        self.__color_picker_dialog.setCurrentColor(self.__current_color)
        self.__color_picker_dialog.currentColorChanged.connect(
            lambda color: self.current_color_changed.emit(self.index, color)
        )
        self.__color_picker_dialog.finished.connect(self.done)

        self.__show_color_picker_button = QPushButton(
            "Color...", default=False, autoDefault=False, parent=self
        )
        self.__show_color_picker_button.clicked.connect(
            lambda: self.__color_picker_dialog.show()
        )

        self.__name_line_edit = QLineEdit(self.__name, parent=self)
        self.__name_line_edit.textEdited.connect(
            lambda new_text: self.current_name_changed.emit(self.index, new_text)
        )

        self.__main_layout = QHBoxLayout()
        self.__main_layout.addWidget(self.__show_color_picker_button)
        self.__main_layout.addWidget(self.__name_line_edit)
        self.setLayout(self.__main_layout)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name
        self.__name_line_edit.setText(self.__name)

    @property
    def current_color(self):
        return self.__color_picker_dialog.currentColor()

    @current_color.setter
    def current_color(self, color):
        self.__color_picker_dialog.setCurrentColor(color)
