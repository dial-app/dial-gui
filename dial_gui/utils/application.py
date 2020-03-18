# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import os

from PySide2.QtCore import QStandardPaths
import pkg_resources


def version() -> str:
    """Returns the current version of the application."""
    return pkg_resources.require("dial-gui")[0].version


def config_directory() -> str:
    config_directory = QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation)

    if not os.path.isdir(config_directory):
        os.mkdir(config_directory)

    return config_directory


def plugins_directory() -> str:
    plugins_directory = QStandardPaths.locate(
        QStandardPaths.AppConfigLocation, "plugins", QStandardPaths.LocateDirectory
    )

    if not plugins_directory:
        plugins_directory = config_directory() + os.path.sep + "plugins"
        os.mkdir(plugins_directory)

    return plugins_directory
