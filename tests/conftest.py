# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pytest

from dial_core.node_editor import Port
from dial_gui.node_editor import GraphicsConnectionFactory
from dial_gui.node_editor.graphics_node import GraphicsPortFactory

collect_ignore = ["setup.py"]


@pytest.fixture
def graphics_port_a():
    return GraphicsPortFactory(port=Port(name="a", port_type=int))


@pytest.fixture
def graphics_port_b():
    return GraphicsPortFactory(port=Port(name="b", port_type=int))


@pytest.fixture
def graphics_connection():
    return GraphicsConnectionFactory()
