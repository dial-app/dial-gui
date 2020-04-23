# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:
"""
Functions to check that python versions, libraries... used by the program are correct.
"""


import json
import os
import signal
import sys
from typing import TYPE_CHECKING

import dial_core
import pkg_resources
from dial_core.plugin import PluginManagerSingleton
from dial_core.utils import log

from . import application

if TYPE_CHECKING:
    import argparse


LOGGER = log.get_logger(__name__)


def initialize(args: "argparse.Namespace"):
    """Performs all the necessary steps before running the application. This checks
    python version, installed modules, graphics configurations, initialize logging
    system...

    Raises:
        ImportError: If couldn't import a necessary module.
        SystemError: If the Python version isn't compatible.
    """
    try:

        dial_core.utils.initialization.initialize(args)
        __gui_initialization(args)

    except (ImportError, SystemError) as err:
        LOGGER.exception(err)

        import tkinter as tk
        from tkinter import messagebox

        tk.Tk().withdraw()
        messagebox.showerror("Error", str(err))

        sys.exit(1)


def __gui_initialization(args: "argparse.Namespace"):
    """Performs all the initialization of the GUI components.

    Args:
        args: App configuration namespace."""
    # State the signals handled by this application
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Necessary for Qt Web Engine
    from PySide2.QtCore import Qt, QCoreApplication
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

    # Initialize PySide2
    from PySide2.QtWidgets import QApplication

    app = QApplication()
    app.setApplicationName("dial")
    app.aboutToQuit.connect(exit_application)

    from dial_gui.project import ProjectManagerGUISingleton
    __plugins_initialization(args)


def __plugins_initialization(args: "argparse.Namespace"):
    """Initializes the plugin manager and loads all the necessary plugins.
    """
    plugins_install_abs_path = os.path.abspath(application.plugins_install_directory())

    sys.path.append(plugins_install_abs_path)
    pkg_resources.working_set.add_entry(plugins_install_abs_path)

    LOGGER.info("%s added to sys.path", plugins_install_abs_path)

    plugins_manager = PluginManagerSingleton(
        application.installed_plugins_file_content()
    )

    LOGGER.debug("Installed plugins: %s", plugins_manager.installed_plugins)

    for plugin in plugins_manager.installed_plugins.values():
        try:
            if plugin.active:
                plugin.load()
        except ModuleNotFoundError as err:
            LOGGER.exception(err)


def exit_application():
    """Cleans up resources and makes modifications before closing the application.

    Important:
        Up to this point, the user can't interact with the GUI. For clean up tasks that
        require the user to interact with, see 'MainWindow.closeEvent' method.
    """
    # Save plugin manager current state
    plugins_manager = PluginManagerSingleton()

    with open(application.installed_plugins_file(), "w") as plugins_file:
        json.dump(plugins_manager.to_dict(), plugins_file, indent=2)

    # Close the PySide2 application
    from PySide2.QtWidgets import QApplication

    QApplication.quit()

    LOGGER.info("Dial closed.")
