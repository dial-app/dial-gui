# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.providers as providers

from dial_core.project import Project

from .project_manager_gui import ProjectManagerGUI

ProjectManagerGUISingleton = providers.Singleton(
    ProjectManagerGUI, default_project=Project()
)
