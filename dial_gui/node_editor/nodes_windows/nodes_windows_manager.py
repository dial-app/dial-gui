# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers
from PySide2.QtCore import QObject, Signal

from .nodes_window import NodesWindow, NodesWindowFactory


class NodesWindowsManager(QObject):
    new_nodes_window_created = Signal(NodesWindow)
    nodes_window_added = Signal(NodesWindow)
    nodes_window_removed = Signal(NodesWindow)

    def __init__(
        self, nodes_windows_factory: "providers.Factory", parent: "QObject" = None
    ):
        super().__init__(parent)

        self.__nodes_windows_factory = nodes_windows_factory
        self.__nodes_windows = []

    @property
    def nodes_windows(self):
        return self.__nodes_windows

    def new_nodes_window(self, name=None) -> "NodesWindow":
        if not name:
            name = f"Nodes Window {len(self.__nodes_windows) + 1}"

        nodes_window = self._new_nodes_impl(name)

        return self.add_nodes_window(nodes_window)

    def add_nodes_window(self, nodes_window: "NodesWindow") -> "NodesWindow":
        return self._add_nodes_window_impl(nodes_window)

    def remove_nodes_window(self, nodes_window: "NodesWindow"):
        self._remove_nodes_window_impl(nodes_window)

    def __reduce__(self):
        return (NodesWindowsManager, (self.__nodes_windows_factory,))

    def _new_nodes_impl(self, name) -> "NodesWindow":
        nodes_window = self.__nodes_windows_factory(name=name)
        self.new_nodes_window_created.emit(nodes_window)
        return nodes_window

    def _add_nodes_window_impl(self, nodes_window: "NodesWindow"):
        self.__nodes_windows.append(nodes_window)
        self.nodes_window_added.emit(nodes_window)
        return nodes_window

    def _remove_nodes_window_impl(self, nodes_window: "NodesWindow"):
        try:
            self.__nodes_windows.remove(nodes_window)
            self.nodes_window_removed.emit(nodes_window)
            nodes_window.clear()

        except ValueError:
            pass


NodesWindowsManagerFactory = providers.Factory(
    NodesWindowsManager, nodes_windows_factory=NodesWindowFactory.delegate()
)
