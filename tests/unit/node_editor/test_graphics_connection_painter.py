# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from unittest.mock import patch

from PySide2.QtCore import Qt
from PySide2.QtGui import QColor, QPen


def test_color(graphics_connection):
    assert graphics_connection.painter.color.name() == "#000000"

    graphics_connection.painter.color = QColor("#444444")

    assert graphics_connection.painter.color.name() == "#444444"


@patch("PySide2.QtGui.QPainter")
def test_paint(mock_qpainter, graphics_connection):
    graphics_connection.painter.color = QColor("#444444")

    graphics_connection.painter.paint(mock_qpainter, None, None)

    mock_qpainter.setBrush.assert_called_once_with(Qt.NoBrush)

    pen = QPen(graphics_connection.painter.color)
    pen.setWidth(graphics_connection.width)
    mock_qpainter.setPen.assert_called_once_with(pen)
