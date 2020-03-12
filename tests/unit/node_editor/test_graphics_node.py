# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pickle

from PySide2.QtWidgets import QGraphicsItem

from dial_gui.node_editor import GraphicsConnectionFactory


def test_title(qtbot, graphics_node_a):
    assert hasattr(graphics_node_a, "title")
    assert graphics_node_a.title == "a"


def test_graphics_ports_created(qtbot, graphics_node_a):
    assert len(graphics_node_a._input_graphics_ports) == 2
    assert len(graphics_node_a._output_graphics_ports) == 2


def test_selected_z_value(qtbot, graphics_node_a, graphics_node_b):
    graphics_node_a.itemChange(QGraphicsItem.ItemSelectedChange, True)
    graphics_node_b.itemChange(QGraphicsItem.ItemSelectedChange, False)

    assert graphics_node_a.zValue() > graphics_node_b.zValue()

    graphics_node_a.itemChange(QGraphicsItem.ItemSelectedChange, False)
    graphics_node_b.itemChange(QGraphicsItem.ItemSelectedChange, True)

    assert graphics_node_a.zValue() < graphics_node_b.zValue()


def test_pickable(qtbot, graphics_node_a, graphics_node_b):
    graphics_node_a.setPos(100, 200)
    graphics_node_b.setPos(40, 760)

    connection1 = GraphicsConnectionFactory()
    connection1.start_graphics_port = graphics_node_a.outputs["out_str"]
    connection1.end_graphics_port = graphics_node_b.inputs["in_str"]

    connection2 = GraphicsConnectionFactory()
    connection2.start_graphics_port = graphics_node_a.outputs["out_int"]
    connection2.end_graphics_port = graphics_node_b.inputs["in_int"]

    obj = pickle.dumps(graphics_node_a)
    loaded_graphics_node_a = pickle.loads(obj)

    # Pos saved
    assert loaded_graphics_node_a.pos() == graphics_node_a.pos()

    # Geometry saved
    # TODO

    # Graphics Ports saved
    assert len(loaded_graphics_node_a.inputs) == 2
    assert len(loaded_graphics_node_a.outputs) == 2

    # Graphics Connections saved
    graphics_out_str = loaded_graphics_node_a.outputs["out_str"]
    assert len(graphics_out_str.graphics_connections) == 1
    graphics_out_int = loaded_graphics_node_a.outputs["out_int"]
    assert len(graphics_out_int.graphics_connections) == 1

    # Underlying ports connected
    graphics_connection_1 = graphics_out_str.graphics_connections[0]
    assert (
        graphics_connection_1.start_graphics_port._port
        in graphics_connection_1.end_graphics_port._port.connections
    )
