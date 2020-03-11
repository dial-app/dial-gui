# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from dial_core.node_editor import Node
from dial_gui.node_editor import GraphicsConnectionFactory, GraphicsNodeFactory


def test_compose_graphics_scene(qtbot):
    node_a = Node(title="node_a")
    node_a.add_input_port(name="in", port_type=int)
    node_a.add_output_port(name="out", port_type=int)

    node_b = Node(title="node_b")
    node_b.add_input_port(name="in", port_type=int)
    node_b.add_output_port(name="out", port_type=int)

    # Graphics Nodes
    graphics_node_a = GraphicsNodeFactory(node_a)
    graphics_node_b = GraphicsNodeFactory(node_b)

    # Graphics Connections
    graphics_connection = GraphicsConnectionFactory()
    graphics_connection.start_graphics_port = graphics_node_a._output_graphics_ports[
        "out"
    ]
    graphics_connection.end_graphics_port = graphics_node_b._input_graphics_ports["in"]

    assert len(graphics_node_a._output_graphics_ports["out"].graphics_connections) == 1
    assert len(graphics_node_b._input_graphics_ports["in"].graphics_connections) == 1


def test_compose_graphics_scene_from_connected_nodes(qtbot):
    node_a = Node(title="node_a")
    node_a.add_output_port(name="out", port_type=int)

    node_b = Node(title="node_b")
    node_b.add_input_port(name="in1", port_type=int)
    node_b.add_input_port(name="in2", port_type=int)

    node_a.outputs["out"].connect_to(node_b.inputs["in1"])
    node_a.outputs["out"].connect_to(node_b.inputs["in2"])

    assert node_a.outputs["out"] in node_b.inputs["in1"].connections
    assert node_a.outputs["out"] in node_b.inputs["in2"].connections

    graphics_node_a = GraphicsNodeFactory(node_a)
    graphics_node_b = GraphicsNodeFactory(node_b)

    assert graphics_node_a._output_graphics_ports["out"]
    assert graphics_node_b._input_graphics_ports["in1"]
    assert graphics_node_b._input_graphics_ports["in2"]

    # TODO: Solve here
    assert len(graphics_node_a._output_graphics_ports["out"].graphics_connections) == 2
