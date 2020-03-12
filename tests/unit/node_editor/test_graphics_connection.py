# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pickle

from PySide2.QtCore import QPointF


def test_start(qtbot, connection_item):
    pos = QPointF(200, 100)
    connection_item.start = pos

    assert connection_item.start == pos
    assert connection_item.start_graphics_port is None


def test_start_graphics_port(qtbot, connection_item, graphics_port_a):
    pos = QPointF(200, 100)

    graphics_port_a.setPos(pos)

    connection_item.start_graphics_port = graphics_port_a
    assert connection_item.start_graphics_port == graphics_port_a
    assert connection_item.start == pos

    assert connection_item.painter.color == graphics_port_a.painter.color


def test_start_replace_port(qtbot, connection_item, graphics_port_a):
    pos = QPointF(100, 150)

    connection_item.start_graphics_port = graphics_port_a

    connection_item.start = pos
    assert connection_item.start == pos
    assert connection_item.start_graphics_port is None


def test_set_start_port_as_none(qtbot, connection_item, graphics_port_a):
    pos = QPointF(200, 100)

    graphics_port_a.setPos(pos)

    connection_item.start_graphics_port = graphics_port_a
    connection_item.start_graphics_port = None

    assert connection_item.start == pos
    assert connection_item.start_graphics_port is None


def test_end(qtbot, connection_item):
    pos = QPointF(200, 100)
    connection_item.end = pos

    assert connection_item.end == pos
    assert connection_item.end_graphics_port is None


def test_end_graphics_port(qtbot, connection_item, graphics_port_a):
    pos = QPointF(200, 100)

    graphics_port_a.setPos(pos)

    connection_item.end_graphics_port = graphics_port_a
    assert connection_item.end_graphics_port == graphics_port_a
    assert connection_item.end == pos


def test_end_replace_port(qtbot, connection_item, graphics_port_a):
    pos = QPointF(100, 150)

    connection_item.end_graphics_port = graphics_port_a

    connection_item.end = pos
    assert connection_item.end == pos
    assert connection_item.end_graphics_port is None


def test_set_end_port_as_none(qtbot, connection_item, graphics_port_a):
    pos = QPointF(200, 100)

    graphics_port_a.setPos(pos)

    connection_item.end_graphics_port = graphics_port_a
    connection_item.end_graphics_port = None

    assert connection_item.end == pos
    assert connection_item.end_graphics_port is None


def test_connect_graphics_port(
    qtbot, connection_item, graphics_port_a, graphics_port_b
):
    connection_item.start_graphics_port = graphics_port_a
    assert connection_item in graphics_port_a.graphics_connections
    assert len(graphics_port_a._port.connections) == 0

    connection_item.end_graphics_port = graphics_port_b
    assert connection_item in graphics_port_b.graphics_connections

    assert graphics_port_a._port in graphics_port_b._port.connections
    assert graphics_port_b._port in graphics_port_a._port.connections


def test_remove_connection(qtbot, connection_item, graphics_port_a, graphics_port_b):
    connection_item.start_graphics_port = graphics_port_a

    # Connection item is in port a
    assert connection_item in graphics_port_a.graphics_connections
    assert connection_item not in graphics_port_b.graphics_connections

    # Underlying ports are still not connected
    assert graphics_port_a._port not in graphics_port_b._port.connections
    assert graphics_port_b._port not in graphics_port_a._port.connections

    connection_item.end_graphics_port = graphics_port_b

    # Connection item is in ports a and b
    assert connection_item in graphics_port_a.graphics_connections
    assert connection_item in graphics_port_b.graphics_connections

    # Underlying ports are connected
    assert graphics_port_a._port in graphics_port_b._port.connections
    assert graphics_port_b._port in graphics_port_a._port.connections

    connection_item.start_graphics_port = None

    # Connection item is in port b only
    assert connection_item not in graphics_port_a.graphics_connections
    assert connection_item in graphics_port_b.graphics_connections

    # Underlying ports are disconnected too
    assert graphics_port_a._port not in graphics_port_b._port.connections
    assert graphics_port_b._port not in graphics_port_a._port.connections

    connection_item.end_graphics_port = None

    # Connection item isn't in any port
    assert connection_item not in graphics_port_a.graphics_connections
    assert connection_item not in graphics_port_b.graphics_connections

    # Underlying ports are still disconnected
    assert graphics_port_a._port not in graphics_port_b._port.connections
    assert graphics_port_b._port not in graphics_port_a._port.connections


def test_pickable(qtbot, connection_item, graphics_port_a, graphics_port_b):
    start_pos = QPointF(200, 100)
    end_pos = QPointF(100, 500)

    graphics_port_a.setPos(start_pos)
    graphics_port_b.setPos(end_pos)

    connection_item.start_graphics_port = graphics_port_a
    connection_item.end_graphics_port = graphics_port_b

    assert connection_item.start == start_pos
    assert connection_item.end == end_pos
    assert connection_item.start_graphics_port == graphics_port_a
    assert connection_item.end_graphics_port == graphics_port_b

    obj = pickle.dumps(connection_item)
    loaded_graphics_connection = pickle.loads(obj)

    assert loaded_graphics_connection.start == start_pos
    assert loaded_graphics_connection.end == end_pos
    assert loaded_graphics_connection.start_graphics_port == graphics_port_a
    assert loaded_graphics_connection.end_graphics_port == graphics_port_b
