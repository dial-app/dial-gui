# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QDialog, QVBoxLayout

from .notebook_editor_widget import NotebookEditorWidgetFactory

if TYPE_CHECKING:
    from .notebook_editor_widget import NotebookEditorWidget
    from PySide2.QtWidgets import QWidget


class NotebookEditorDialog(QDialog):
    def __init__(
        self, notebook_editor_widget: "NotebookEditorWidget", parent: "QWidget" = None
    ):
        super().__init__(parent)

        self.setWindowTitle("Notebook Editor")

        self.__notebook_editor_widget = notebook_editor_widget

        self.__main_layout = QVBoxLayout()
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.__main_layout.addWidget(self.__notebook_editor_widget)

        self.setLayout(self.__main_layout)

    def sizeHint(self) -> "QSize":
        """Preferred size of this dialog."""
        return QSize(800, 600)


NotebookEditorDialogFactory = providers.Factory(
    NotebookEditorDialog, notebook_editor_widget=NotebookEditorWidgetFactory
)
