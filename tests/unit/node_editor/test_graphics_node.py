# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtWidgets import QGraphicsItem


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
