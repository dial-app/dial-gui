# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from unittest.mock import patch

from PySide2.QtCore import Qt
from PySide2.QtGui import QColor, QPen


def test_color(connection_item):
    assert connection_item.painter.color.name() == "#000000"

    connection_item.painter.color = QColor("#444444")

    assert connection_item.painter.color.name() == "#444444"


@patch("PySide2.QtGui.QPainter")
def test_paint(mock_qpainter, connection_item):
    connection_item.painter.color = QColor("#444444")

    connection_item.painter.paint(mock_qpainter, None, None)

    mock_qpainter.setBrush.assert_called_once_with(Qt.NoBrush)

    pen = QPen(connection_item.painter.color)
    pen.setWidth(connection_item.width)
    mock_qpainter.setPen.assert_called_once_with(pen)
