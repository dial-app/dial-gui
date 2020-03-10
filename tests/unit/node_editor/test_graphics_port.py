# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# import pickle

from PySide2.QtCore import QPointF


def test_graphics_port_attributes(qtbot, graphics_port_a):
    assert hasattr(graphics_port_a, "name")
    assert hasattr(graphics_port_a, "graphics_connections")
    assert hasattr(graphics_port_a, "graphics_node")
    assert hasattr(graphics_port_a, "radius")
    assert hasattr(graphics_port_a, "margin")


# TODO: Fill
# def test_graphics_connections(qtbot, graphics_port_a):
#     pass


def test_bounding_rect(qtbot, graphics_port_a):
    # Center click
    assert graphics_port_a.boundingRect().contains(QPointF(0, 0))

    # Top Left corner (included)
    assert graphics_port_a.boundingRect().contains(
        QPointF(
            -graphics_port_a.radius - graphics_port_a.margin,
            -graphics_port_a.radius - graphics_port_a.margin,
        )
    )

    # Bottom Right corner (included)
    assert graphics_port_a.boundingRect().contains(
        QPointF(
            graphics_port_a.radius + graphics_port_a.margin,
            graphics_port_a.radius + graphics_port_a.margin,
        )
    )


def test_pickable(qtbot, graphics_port_a, graphics_port_b):
    pass
