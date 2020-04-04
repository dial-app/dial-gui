# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import List, Optional

import dependency_injector.providers as providers
from PySide2.QtCore import QObject, Signal

from .nodes_window import NodesWindow, NodesWindowFactory


class NodesWindowsGroup(QObject):
    """The NodesWindowsGroup class provides a container for NodesWindow objects.

    This container allows to group several NodesWindow that are related between them
    (For example, because they're all part of the same Project).

    Attributes:
        nodes_windows: List with all the NodesWindow objects.
    """

    new_nodes_window_created = Signal(NodesWindow)
    nodes_window_added = Signal(NodesWindow)
    nodes_window_removed = Signal(NodesWindow)

    def __init__(
        self,
        default_nodes_windows_factory: "providers.Factory",
        parent: "QObject" = None,
    ):
        super().__init__(parent)

        self.__default_nodes_windows_factory = default_nodes_windows_factory
        self.__nodes_windows = []

    @property
    def nodes_windows(self) -> List["NodesWindow"]:
        """Returns the list of stored NodesWindow objects."""
        return self.__nodes_windows

    def new_nodes_window(self, name: Optional[str] = None) -> "NodesWindow":
        """Constructs a new NodesWindow object and adds it.

        Args:
            name: Name for the new window.

        Returns:
            The created NodesWindow object.
        """
        if not name:
            name = f"Nodes Window {len(self.__nodes_windows) + 1}"

        nodes_window = self._new_nodes_impl(name)

        return self.add_nodes_window(nodes_window)

    def add_nodes_window(self, nodes_window: "NodesWindow") -> "NodesWindow":
        """Adds an existent NodesWindow object to the group.

        Returns:
            The added NodesWindow object.
        """
        return self._add_nodes_window_impl(nodes_window)

    def remove_nodes_window(self, nodes_window: "NodesWindow"):
        """Removes a NodesWindow object from the group.

        If the object isn't found, this method doesn't throw any exception.
        """
        self._remove_nodes_window_impl(nodes_window)

    def _new_nodes_impl(self, name) -> "NodesWindow":
        """Implementation of the node creation operation.

        Sends a `new_nodes_window_created` signal.

        Returns:
            The created NodesWindow object.
        """
        nodes_window = self.__default_nodes_windows_factory(name=name)
        self.new_nodes_window_created.emit(nodes_window)
        return nodes_window

    def _add_nodes_window_impl(self, nodes_window: "NodesWindow") -> "NodesWindow":
        """Implementation of the node addition operation.

        Sends a `nodes_window_added` signal after the element is inserted.

        Returns:
            The added NodesWindow object.
        """
        self.__nodes_windows.append(nodes_window)
        self.nodes_window_added.emit(nodes_window)
        return nodes_window

    def _remove_nodes_window_impl(self, nodes_window: "NodesWindow"):
        """Implementation of the NodesWindow removal operation.

        Sends a `nodes_window_removed` signal after the element is removed.
        """
        try:
            self.__nodes_windows.remove(nodes_window)
            self.nodes_window_removed.emit(nodes_window)
            nodes_window.clear()

        except ValueError:
            pass

    def __reduce__(self):
        return (NodesWindowsGroup, (self.__default_nodes_windows_factory,))


NodesWindowsGroupFactory = providers.Factory(
    NodesWindowsGroup, default_nodes_windows_factory=NodesWindowFactory.delegate()
)
