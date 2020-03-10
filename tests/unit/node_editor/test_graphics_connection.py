# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pickle
from unittest.mock import patch

from PySide2.QtCore import QPointF
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QGraphicsItem


def test_start(qtbot, graphics_connection):
    pos = QPointF(200, 100)
    graphics_connection.start = pos

    assert graphics_connection.start == pos
    assert graphics_connection.start_graphics_port is None


def test_start_graphics_port(qtbot, graphics_connection, graphics_port_a):
    pos = QPointF(200, 100)

    graphics_port_a.setPos(pos)

    graphics_connection.start_graphics_port = graphics_port_a
    assert graphics_connection.start_graphics_port == graphics_port_a
    assert graphics_connection.start == pos

    assert graphics_connection.painter.color == graphics_port_a.painter.color


def test_start_replace_port(qtbot, graphics_connection, graphics_port_a):
    pos = QPointF(100, 150)

    graphics_connection.start_graphics_port = graphics_port_a

    graphics_connection.start = pos
    assert graphics_connection.start == pos
    assert graphics_connection.start_graphics_port is None


def test_set_start_port_as_none(qtbot, graphics_connection, graphics_port_a):
    pos = QPointF(200, 100)

    graphics_port_a.setPos(pos)

    graphics_connection.start_graphics_port = graphics_port_a
    graphics_connection.start_graphics_port = None

    assert graphics_connection.start == pos
    assert graphics_connection.start_graphics_port is None


def test_end(qtbot, graphics_connection):
    pos = QPointF(200, 100)
    graphics_connection.end = pos

    assert graphics_connection.end == pos
    assert graphics_connection.end_graphics_port is None


def test_end_graphics_port(qtbot, graphics_connection, graphics_port_a):
    pos = QPointF(200, 100)

    graphics_port_a.setPos(pos)

    graphics_connection.end_graphics_port = graphics_port_a
    assert graphics_connection.end_graphics_port == graphics_port_a
    assert graphics_connection.end == pos


def test_end_replace_port(qtbot, graphics_connection, graphics_port_a):
    pos = QPointF(100, 150)

    graphics_connection.end_graphics_port = graphics_port_a

    graphics_connection.end = pos
    assert graphics_connection.end == pos
    assert graphics_connection.end_graphics_port is None


def test_set_end_port_as_none(qtbot, graphics_connection, graphics_port_a):
    pos = QPointF(200, 100)

    graphics_port_a.setPos(pos)

    graphics_connection.end_graphics_port = graphics_port_a
    graphics_connection.end_graphics_port = None

    assert graphics_connection.end == pos
    assert graphics_connection.end_graphics_port is None


def test_item_change(qtbot, graphics_connection):
    color = QColor("#444444")

    graphics_connection.painter.color = color

    graphics_connection.itemChange(QGraphicsItem.ItemSelectedChange, value=True)

    assert graphics_connection.painter.color != color


# TODO: Test that underlying port is connected
# def test_port_connected(qtbot, graphics_connection, graphics_port_a, graphics_port_b):
#       pass


def test_pickable(qtbot, graphics_connection, graphics_port_a, graphics_port_b):
    start_pos = QPointF(200, 100)
    end_pos = QPointF(100, 500)

    graphics_port_a.setPos(start_pos)
    graphics_port_b.setPos(end_pos)

    graphics_connection.start_graphics_port = graphics_port_a
    graphics_connection.end_graphics_port = graphics_port_b

    assert graphics_connection.start == start_pos
    assert graphics_connection.end == end_pos
    assert graphics_connection.start_graphics_port == graphics_port_a
    assert graphics_connection.end_graphics_port == graphics_port_b

    obj = pickle.dumps(graphics_connection)
    loaded_graphics_connection = pickle.loads(obj)

    assert loaded_graphics_connection.start == start_pos
    assert loaded_graphics_connection.end == end_pos
    assert loaded_graphics_connection.start_graphics_port == graphics_port_a
    assert loaded_graphics_connection.end_graphics_port == graphics_port_b
