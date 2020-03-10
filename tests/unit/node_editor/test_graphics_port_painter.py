# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


from unittest.mock import patch


def test_paint_area(qtbot, graphics_port_a):
    # Center
    assert graphics_port_a.painter.paint_area().contains(0, 0)

    # Top left corner
    assert graphics_port_a.painter.paint_area().contains(
        -graphics_port_a.radius, -graphics_port_a.radius
    )

    # Bottom Right corner
    assert graphics_port_a.painter.paint_area().contains(
        graphics_port_a.radius, graphics_port_a.radius
    )


@patch("PySide2.QtGui.QPainter")
def test_paint(mock_qpainter, qtbot, graphics_port_a):
    graphics_port_a.painter.paint(mock_qpainter, None, None)

    mock_qpainter.drawEllipse.assert_called_once_with(
        graphics_port_a.painter.paint_area()
    )
