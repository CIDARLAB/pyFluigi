from pymint.mintdevice import MINTDevice


def assign_single_port_terminals(mint_device: MINTDevice):
    # Loop through each of the connections
    for connection in mint_device.device.connections:

        # Check if the connection has a source
        if connection.source is None:
            raise ValueError("Source of connection {} is None".format(connection.ID))

        # Check if the source component has a single port
        source_component = mint_device.device.get_component(connection.source.component)

        if None is connection.source.port and len(source_component.ports) == 1:
            connection.source.port = source_component.ports[0].label

        for sink_target in connection.sinks:
            sink_component = mint_device.device.get_component(sink_target.component)

            if None is sink_target.port and len(sink_component.ports) == 1:
                sink_target.port = sink_component.ports[0].label
