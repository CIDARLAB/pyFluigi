import sys
from typing import List, Union
from parchmint.target import Target
from pymint.mintdevice import MINTDevice
from parchmint.device import Device
from parchmint.component import Component
from pymint.mintcomponent import MINTComponent

# Step 3 - Modify the rotation of the newly placed component to reduce the distance between source and sink ports


def distance_between_port_wall(
    device,
    center_target: Target,
    wall_x: int,
):
    # Get the component
    component1 = device.get_component(center_target.component)
    component1.rotate_component()
    pos1 = component1.get_absolute_port_coordinates(center_target.port)
    pos2 = (wall_x, 0)
    distance = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    return distance


def distance_between_ports(
    device,
    center_target: Target,
    wall_target: Target,
):
    # Get the component
    component1 = device.get_component(center_target.component)
    component2 = device.get_component(wall_target.component)
    pos1 = component1.get_absolute_port_coordinates(center_target.port)
    pos2 = component2.get_absolute_port_coordinates(wall_target.port)
    distance = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    return distance


def align_y_to_center(component1, component2):
    # Align component1's center y to component2's center y
    component2.ypos = component1.ypos - abs(component1.yspan / 2 - component2.yspan / 2)


def get_predecessor_distance(
    device: Union[MINTDevice, Device], chain: List[str], node: str, other: str
):
    # Set the predecessor window to be on the EAST side of the node at the center of the compoent in y-direction

    # Get the component
    pred_component = device.get_component(other)
    current_component = device.get_component(node)
    # Get the total distance between the source and sink ports
    # after aligning source and sink components along the centers of the components
    current_component.xpos = 0
    current_component.ypos = -current_component.yspan / 2

    # Get the distance between the source and sink ports
    distance = 0
    # Get the edge between the predecessor and the node
    connections = device.get_connections_for_edge(pred_component, current_component)

    for connection in connections:
        source_target = connection.source
        if source_target is None:
            continue
        if source_target.component not in chain:
            continue
        for sink_target in connection.sinks:
            if sink_target.component not in chain:
                continue
            distance += distance_between_port_wall(
                device=device,
                center_target=sink_target,
                wall_x=(
                    current_component.xpos - 3 * current_component.component_spacing
                ),
            )

    return distance


def get_successor_distance(
    device: Union[MINTDevice, Device], chain: List[str], node: str, other: str
):
    # Set the predecessor window to be on the EAST side of the node at the center of the compoent in y-direction

    # Get the component
    suc_component = device.get_component(other)
    current_component = device.get_component(node)
    # Get the total distance between the source and sink ports
    # after aligning source and sink components along the centers of the components
    current_component.xpos = 0
    current_component.ypos = -current_component.yspan / 2

    # Get the distance between the source and sink ports
    distance = 0
    # Get the edge between the predecessor and the node
    connections = device.get_connections_for_edge(current_component, suc_component)

    for connection in connections:
        source_target = connection.source
        # check if the source_target component is inside the DFS chain
        if source_target is None:
            continue
        if source_target.component not in chain:
            continue
        for sink_target in connection.sinks:
            if sink_target.component not in chain:
                continue
            distance += distance_between_port_wall(
                device,
                center_target=source_target,
                wall_x=(
                    current_component.xpos
                    + current_component.xspan
                    + 3 * current_component.component_spacing
                ),
            )

    return distance


def step_3_1(device, stem_graph, levels, dfs_chains):
    # go through each of the dfs chains
    for chain in dfs_chains:
        # go through each of the nodes in the dfs chain
        for node in chain:
            # Try rotation values 0, 90, 180, 270 to see if the distance between the source and sink ports is reduced, and keep
            # the one which has the least distance
            min_distance = sys.maxsize
            min_rotation = 0
            # Get predecessors and successors of the node
            predecessors = list(stem_graph.predecessors(node))
            successors = list(stem_graph.successors(node))
            node_component = device.get_component(node)

            for rotation in [0, 90, 180, 270]:
                # rotate the node (assume that the right orientation of the component is used later on in the distance calculation)
                node_component.rotation = rotation

                # get the distance between the source and sink ports
                distance = sum(
                    [
                        get_predecessor_distance(device, chain, node, predecessor)
                        for predecessor in predecessors
                    ]
                ) + sum(
                    [
                        get_successor_distance(device, chain, node, successor)
                        for successor in successors
                    ]
                )
                # if the distance is less than the previous distance, then save the new distance and rotation
                print(
                    "Distance for component {}:{} - {}".format(node, rotation, distance)
                )
                if distance < min_distance:
                    min_distance = distance
                    min_rotation = rotation

            # Rotate the node to the min rotation
            node_component.rotation = min_rotation

    # print out all the component rotations on the stem graph
    for node in stem_graph.nodes():
        component = device.get_component(node)
        print("Component {} rotation: {}".format(node, component.rotation))

def step_3_2():
    pass