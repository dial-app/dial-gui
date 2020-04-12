# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import json
import os
from typing import Optional

import pkg_resources
from PySide2.QtCore import QStandardPaths


def version() -> str:
    """Returns the current version of the application."""
    return pkg_resources.require("dial-gui")[0].version


def config_directory() -> str:
    """Returns the configuration directory (This is the root dir for dial)"""
    config_directory = (
        QStandardPaths.writableLocation(QStandardPaths.ConfigLocation)
        + os.path.sep
        + "dial"
    )

    if not os.path.isdir(config_directory):
        os.mkdir(config_directory)

    return config_directory


def plugins_directory() -> str:
    """Returns the root directory for dial plugins (Where the `plugins.json` file is)"""
    plugins_directory = config_directory() + os.path.sep + "plugins"

    if not os.path.isdir(plugins_directory):
        os.mkdir(plugins_directory)

    return plugins_directory


def plugins_install_directory() -> str:
    """Returns the directory where plugins are installed."""
    plugins_install_directory = plugins_directory() + os.path.sep + "site-packages"

    if not os.path.isdir(plugins_install_directory):
        os.mkdir(plugins_install_directory)

    return plugins_install_directory


def installed_plugins_file() -> str:
    """Returns the file that contains which plugins are installed and active."""
    plugins_file_path = plugins_directory() + os.path.sep + "plugins.json"

    if not os.path.isfile(plugins_file_path):
        with open(plugins_file_path, "w") as json_file:
            json.dump({}, json_file)

    return plugins_file_path


def installed_plugins_file_content() -> Optional[dict]:
    """Returns the content of the `plugins.json` file."""
    with open(installed_plugins_file()) as plugins_file:
        return json.load(plugins_file)

    return None
