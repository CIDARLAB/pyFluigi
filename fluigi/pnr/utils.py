import sys

from parchmint.device import Device
from pymint import MINTDevice


def size_nodes(mint_device: MINTDevice) -> None:
    if mint_device.device.graph is None:
        raise ValueError("MINT Device is None")
    for component in mint_device.device.components:
        if component.entity == "NODE":
            # Look at the connections
            nbers = mint_device.device.graph.edges(component.ID)
            gedges = list(nbers)
            if len(gedges) > 0:
                gedge = gedges[0]
            else:
                print("No edges connected to NODE {0}".format(component.ID))
                continue
            # Get channelWidth from there and update the node
            # connection_ref = device.G[gedge[0]][gedge[1]]
            connection = mint_device.device.graph.get_edge_data(gedge[0], gedge[1])[0]["connection_ref"]
            channel_width = connection.params.get_param("channelWidth")
            component.xspan = channel_width
            component.yspan = channel_width


def check_ref_and_assign_port(source_ref, connection, device: Device, global_port_assign_map):
    source_name = source_ref.component
    source = device.get_component(source_name)
    if source_ref.port is None:
        print("No port assigned to connection ref - {}:{}:{}".format(connection.ID, source.ID, source_ref.port))
        if len(source.ports) == 1:
            print("Auto Port Assign Scheme - Target contains only 1 port option")
            source_ref.port = source.ports[0].label
        elif len(source.ports) == 2 or len(source.ports) == 4:
            print("Auto Port Assign Scheme - Target contains only 2 or 4 port options")
            if source.ID not in global_port_assign_map.keys():
                # Add component to global assign map
                global_port_assign_map[source.ID] = 0

            # Do the assignment of the port from the global assign map index
            port_index = global_port_assign_map[source.ID]
            source_ref.port = str(source.ports[port_index].label)
            port_index += 1
        else:
            print("Error - Auto Port scheme does not work for target containing {} ports ".format(len(source.ports)))

        print("Assigned port - {}".format(source_ref.port))


def assign_component_ports(mint_device: MINTDevice) -> None:
    print("Starting terminal/port assignment ...")
    global_port_assign_map = dict()
    for connection in mint_device.device.connections:
        source_ref = connection.source
        check_ref_and_assign_port(source_ref, connection, mint_device.device, global_port_assign_map)
        for sink_ref in connection.sinks:
            check_ref_and_assign_port(sink_ref, connection, mint_device.device, global_port_assign_map)


def reduce_device_size(device: Device, design_padding: int) -> None:

    print("Reducing the Size of the device and adding device padding: {} um".format(design_padding))
    # Step 1 - First find the min_x, min_y, max_x, max_y of the design
    min_x = sys.maxsize
    min_y = sys.maxsize
    max_x = -sys.maxsize - 1
    max_y = -sys.maxsize - 1
    for component in device.components:
        if component.xpos < min_x:
            min_x = component.xpos
        if component.ypos < min_y:
            min_y = component.ypos
        if component.xpos + component.xspan > max_x:
            max_x = component.xpos + component.xspan
        if component.ypos + component.ypos > max_y:
            max_y = component.ypos + component.ypos

    # Step 2 - Move all components and connections by design_padding - (minx, miny)
    offset_x = design_padding - min_x
    offset_y = design_padding - min_y

    for component in device.components:
        component.xpos += offset_x
        component.ypos += offset_y

    for connection in device.connections:
        for path in connection.paths:
            new_path = []
            for waypoint in path.waypoints:
                wp = (waypoint[0] + offset_x, waypoint[1] + offset_y)
                new_path.append(wp)
            path.waypoints = new_path

    # Step 3 - Modify the overall device dimensions to max_x + design_padding, max_y + design_padding
    xspan = device.xspan
    yspan = device.yspan

    xspan = max_x + 2 * design_padding
    yspan = max_y + 2 * design_padding

    device.xspan = xspan
    device.yspan = yspan

    print("Updated the device dimensions: ({}, {}) microns".format(xspan, yspan))
