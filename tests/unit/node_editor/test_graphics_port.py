# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QPointF


def test_graphics_port_attributes(qtbot, graphics_port_a):
    assert hasattr(graphics_port_a, "name")
    assert hasattr(graphics_port_a, "port_type")
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


def test_several_conenctions(qtbot, graphics_port_a, graphics_port_b, connection_item):
    connection_item.start_graphics_port = graphics_port_a
    connection_item.end_graphics_port = graphics_port_b

    # connection_item_2 = deepcopy(connection_item)

    assert len(graphics_port_a.graphics_connections) == 1
    assert len(graphics_port_b.graphics_connections) == 1


#     graphics_port_a.add_connection(connection_item_2)

#     assert len(graphics_port_a.graphics_connections) == 1
#     assert len(graphics_port_b.graphics_connections) == 1


def test_pickable(qtbot, graphics_port_a, graphics_port_b):
    pass
