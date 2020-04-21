# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers
from dial_core.notebook import NotebookProjectGenerator, NotebookProjectGeneratorFactory
from dial_gui.project import ProjectGUI, ProjectManagerGUI, ProjectManagerGUISingleton
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtWidgets import QPushButton, QVBoxLayout, QWidget

from nbconvert import HTMLExporter


class NotebookEditorWidget(QWidget):
    """The NotebookEditorWidget class provides an interface for visualizing the graph as
    a Jupyter Notebook, HTML rendered."""

    def __init__(
        self,
        notebook_generator: "NotebookProjectGenerator",
        project_manager: "ProjectManagerGUI",
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        # Components
        self._project_manager = project_manager
        self._notebook_generator = notebook_generator

        self._project_manager.active_project_changed.connect(self._set_active_project)

        # Widgets
        self._text_browser = QWebEngineView()
        self._text_browser.show()

        self._generate_notebook_button = QPushButton("Generate Notebook")
        self._generate_notebook_button.clicked.connect(self._generate_html)

        # Layout
        self._main_layout = QVBoxLayout()
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.addWidget(self._text_browser)
        self._main_layout.addWidget(self._generate_notebook_button)

        self.setLayout(self._main_layout)

        # Set active project and generate notebook
        self._set_active_project(self._project_manager.active)

    def _set_active_project(self, project: "ProjectGUI"):
        """Sets a new active project for this notebook generator."""
        if project is not self._notebook_generator.get_project():
            self._notebook_generator.set_project(project)
            self._generate_html()

    def _generate_html(self):
        """Fills the html viewer with the jupyter notebook html."""
        self._notebook_generator.update_project_changes()

        notebook = self._notebook_generator.notebook

        html_exporter = HTMLExporter()

        (body, resources) = html_exporter.from_notebook_node(notebook)

        html_content = (
            f'<html><style type="text/css">{resources["inlining"]["css"][0]}'
            f"</style><body>{body}</body></html>"
        )

        with open("file.html", "w") as html_file:
            html_file.write(html_content)

        self._notebook_generator.save_notebook_as("nb.ipynb")

        self._text_browser.setHtml(html_content)


NotebookEditorWidgetFactory = providers.Factory(
    NotebookEditorWidget,
    notebook_generator=NotebookProjectGeneratorFactory,
    project_manager=ProjectManagerGUISingleton,
)
