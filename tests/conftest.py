# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pytest

from dial_core.node_editor import Node, Port
from dial_gui.node_editor import GraphicsConnectionFactory, GraphicsNodeFactory
from dial_gui.node_editor.graphics_node import GraphicsPortFactory

collect_ignore = ["setup.py"]


@pytest.fixture
def graphics_port_a():
    return GraphicsPortFactory(port=Port(name="a", port_type=int))


@pytest.fixture
def graphics_port_b():
    return GraphicsPortFactory(port=Port(name="b", port_type=int))


@pytest.fixture
def connection_item():
    return GraphicsConnectionFactory()


@pytest.fixture
def node_a():
    node = Node(title="a")
    node.add_input_port(name="in_int", port_type=int)
    node.add_input_port(name="in_str", port_type=str)
    node.add_output_port(name="out_int", port_type=int)
    node.add_output_port(name="out_str", port_type=int)

    return node


@pytest.fixture
def node_b():
    node = Node(title="b")
    node.add_input_port(name="in_int", port_type=int)
    node.add_input_port(name="in_str", port_type=str)
    node.add_output_port(name="out_int", port_type=int)
    node.add_output_port(name="out_str", port_type=int)

    return node


@pytest.fixture
def graphics_node_a(node_a):
    return GraphicsNodeFactory(node=node_a)


@pytest.fixture
def graphics_node_b(node_b):
    return GraphicsNodeFactory(node=node_b)
