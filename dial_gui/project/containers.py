# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.providers as providers

from dial_gui.node_editor import DefaultGraphicsSceneFactory

from .project_gui import ProjectGUI
from .project_manager_gui import ProjectManagerGUI

DefaultProjectGUI = providers.Factory(
    ProjectGUI, name="Default Project", graphics_scene=DefaultGraphicsSceneFactory
)

ProjectManagerGUISingleton = providers.Singleton(
    ProjectManagerGUI, default_project=DefaultProjectGUI
)
