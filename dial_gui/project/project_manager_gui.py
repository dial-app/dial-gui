# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QObject

from dial_core.project import Project, ProjectManager


class ProjectManagerGUI(QObject, ProjectManager):

    # TODO: Change default project to a ProjectWidget
    def __init__(self, default_project: "Project", parent=None):
        QObject.__init__(self, parent)
        ProjectManager.__init__(self, default_project)

    def open_project(self, file_path: str):
        print("TODO: Start implementing project operators")
