# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Optional

import os
import json

from PySide2.QtCore import QStandardPaths
import pkg_resources


def version() -> str:
    """Returns the current version of the application."""
    return pkg_resources.require("dial-gui")[0].version


def config_directory() -> str:
    config_directory = (
        QStandardPaths.writableLocation(QStandardPaths.ConfigLocation)
        + os.path.sep
        + "dial"
    )

    if not os.path.isdir(config_directory):
        os.mkdir(config_directory)

    return config_directory


def plugins_directory() -> str:
    plugins_directory = config_directory() + os.path.sep + "plugins"

    if not os.path.isdir(plugins_directory):
        os.mkdir(plugins_directory)

    return plugins_directory


def plugins_install_directory() -> str:
    plugins_install_directory = plugins_directory() + os.path.sep + "site-packages"

    if not os.path.isdir(plugins_install_directory):
        os.mkdir(plugins_install_directory)

    return plugins_install_directory


def installed_plugins_file() -> str:
    return plugins_directory() + os.path.sep + "plugins.json"


def installed_plugins_file_content() -> Optional[dict]:
    with open(installed_plugins_file()) as plugins_file:
        return json.load(plugins_file)

    return None
