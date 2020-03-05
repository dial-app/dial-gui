# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pickle

import pytest

from dial_core.node_editor import Port
from dial_gui.node_editor import GraphicsPort


@pytest.fixture
def graphics_port_a():
    return GraphicsPort(
        port=Port(name="A", port_type=int),
        port_name_position=GraphicsPort.PortNamePosition.Right,
    )


def test_graphics_port_attributes(qtbot, graphics_port_a):
    assert hasattr(graphics_port_a, "color")
    assert hasattr(graphics_port_a, "port")
    assert hasattr(graphics_port_a, "connections")
    assert hasattr(graphics_port_a, "radius")
    assert hasattr(graphics_port_a, "outline_pen")


def test_graphics_port_pickle(qtbot, graphics_port_a):
    with open("graphics_port_a.pickle", "wb") as binary_file:
        pickle.dump(graphics_port_a, binary_file, protocol=pickle.HIGHEST_PROTOCOL)

    with open("graphics_port_a.pickle", "rb") as binary_file:
        loaded_graphics_port_a = pickle.load(binary_file)

        test_graphics_port_attributes(qtbot, loaded_graphics_port_a)
