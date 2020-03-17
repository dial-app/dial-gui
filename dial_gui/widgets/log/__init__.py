# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
This package includes several widgets that can be used to display a logging dialog.
"""

from .logger_dialog import LoggerDialogFactory
from .logger_textbox import LoggerTextboxFactory

__all__ = ["LoggerDialogFactory", "LoggerTextboxFactory"]
