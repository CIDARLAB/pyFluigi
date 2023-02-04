from __future__ import annotations
from enum import Enum
from typing import List, Dict, NamedTuple
from parchmint.component import Component
from parchmint.port import Port
from queue import Queue


from fluigi.pnr.sfc.spacer_insert import SpacerInsert
from fluigi.pnr.sfc.primitivecell import PrimitiveCell, ComponentSide


class CompositeCell:
    def __init__(self, cell_list: List[List[PrimitiveCell]]) -> None:
        self._cells = cell_list

    @staticmethod
    def spread_ports(
        cell_list: List[List[PrimitiveCell]],
        side: ComponentSide,
        component: Component,
        ports_list: List[Port],
    ) -> None:
        # First create an a reporesentative array of the active ports on the composite cell side of interest with the ports locations being 1
        # [ ][ ][1][1][1][ ][ ]
        # start with the outer most ports and try to figure hwere I can bin the ports along the array according to their relative locations
        # along the edge

        # Extract the ports side of interest from the composite cell
        spread_array = []
        if side is ComponentSide.NORTH:
            spread_array = [cell.north_port for cell in cell_list[0]]
        elif side is ComponentSide.EAST:
            spread_array = [row[-1].east_port for row in cell_list]
        elif side is ComponentSide.SOUTH:
            spread_array = [cell.south_port for cell in cell_list[-1]]
        else:
            spread_array = [row[0].west_port for row in cell_list]

        # Create a list of the ports locations
        bin_data = generate_bin_map(
            spread_array=spread_array,
            port_list=ports_list,
            component=component,
            side=side,
        )
        try_shift_left(
            spread_array=spread_array,
            binning_data=bin_data,
        )
        try_shift_right(
            spread_array=spread_array,
            binning_data=bin_data,
        )
        try_shift_left(
            spread_array=spread_array,
            binning_data=bin_data,
        )

    @staticmethod
    def activate_ports(
        cell_list: List[List[PrimitiveCell]],
        side: ComponentSide,
        size: int,
        ports_list: List[Port],
    ) -> None:

        # First figure the size of the composite cell so that we know which index we have to loop
        # through to activate the ports
        is_vertical = False
        if side is ComponentSide.EAST or size is ComponentSide.WEST:
            is_vertical = True

        # Next check if the size is odd or even combo and run the corresponding algorithm
        # Case 1 - Odd number of ports and odd size of composite cell - Center is the center, and expand outwards
        # Case 2 - Even number of ports and odd size of composite cell - Skip the center and expand outwards
        # Case 3 - Odd number of ports and even size of composite cell - SKip/Fail - Not applicatble since we avoid this scenario
        # Case 4 - Even number of ports and even size of composite cell - Both the center=floor(size/2) and the center+1
        # are the centers, and expand outwards

        # Find the center
        center = size // 2

        # Case 1
        if size % 2 == 1 and len(ports_list) % 2 == 1:
            # Odd number of ports and odd size of composite cell
            #     o  o  o
            # [ ][ ][ ][ ][ ]
            # Activate the ports
            if is_vertical:
                cell_list[0][center].activate_port(side)
                for offset in range(1, center + 1):
                    cell_list[0][center + offset].activate_port(side)
                    cell_list[0][center - offset].activate_port(side)
            else:
                cell_list[center][0].activate_port(side)
                for offset in range(1, center + 1):
                    cell_list[center + offset][0].activate_port(side)
                    cell_list[center - offset][0].activate_port(side)

        # Case 2
        elif size % 2 == 1 and len(ports_list) % 2 == 0:
            # Even number of ports and odd size of composite cell
            #     o     o
            # [ ][ ][ ][ ][ ]
            # Activate the ports
            if is_vertical:
                for offset in range(1, center + 1):
                    cell_list[0][center + offset].activate_port(side)
                    cell_list[0][center - offset].activate_port(side)
            else:
                for offset in range(1, center + 1):
                    cell_list[center + offset][0].activate_port(side)
                    cell_list[center - offset][0].activate_port(side)

        # Case 4
        elif size % 2 == 0 and len(ports_list) % 2 == 0:
            # Even number of ports and even size of composite cell
            #     o  o
            # [ ][ ][ ][ ]
            # Activate the ports
            if is_vertical:
                for offset in range(0, center):
                    cell_list[0][center + offset + 1].activate_port(side)
                    cell_list[0][center - offset].activate_port(side)
            else:
                for offset in range(0, center):
                    cell_list[center + offset + 1][0].activate_port(side)
                    cell_list[center - offset][0].activate_port(side)

        else:
            # Odd number of ports and even size of composite cell
            # Not applicatble since we avoid this scenario
            raise Exception(
                "Odd number of ports and even size of composite cell is not applicable"
            )

    @staticmethod
    def from_parchmint_component(component: Component) -> CompositeCell:
        # Create a list of lists of primitive cells
        cell_list: List[List[PrimitiveCell]] = []

        # First create lists for all the ports
        # on each of the sides. Based on that
        # generate the correspond n*m composite
        north_ports: List[Port] = []
        east_ports: List[Port] = []
        south_ports: List[Port] = []
        west_ports: List[Port] = []

        # loop through all the ports and add them
        # to the appropriate list
        for port in component.ports:
            closest_side = get_closest_side(component, port)
            if closest_side is ComponentSide.NORTH:
                north_ports.append(port)
            elif closest_side is ComponentSide.EAST:
                east_ports.append(port)
            elif closest_side is ComponentSide.SOUTH:
                south_ports.append(port)
            else:
                west_ports.append(port)

        # Now sort the ports based on their x and y coordinates.
        # West->East and South->North
        north_ports.sort(key=lambda port: port.x)
        east_ports.sort(key=lambda port: port.y)
        south_ports.sort(key=lambda port: port.x)
        west_ports.sort(key=lambda port: port.y)

        # horizontal and vertical side port lists to be used for spacer generation in the end
        horizontal_side_port_lists = [port for port in north_ports]
        horizontal_side_port_lists.extend([port for port in south_ports])

        vertical_side_port_lists = [port for port in east_ports]
        vertical_side_port_lists.extend([port for port in west_ports])

        horizontal_side_port_lists.sort(key=lambda port: port.x)
        vertical_side_port_lists.sort(key=lambda port: port.y)

        # Next, setup the required ports on all
        # the ends based on the generation. If
        # there are odd number of ports on any
        # side generate n+1 size squares
        # and if there are even number of ports
        # generate n size squares

        # X Size of the composite cell
        x_size = max([len(north_ports), len(south_ports)])
        # Y Size of the composite cell
        y_size = max([len(east_ports), len(west_ports)])

        # Now check if the sizes is odd or even and increment if odd
        if len(north_ports) % 2 == 1 or len(south_ports) % 2 == 1:
            x_size += 1
        if len(east_ports) % 2 == 1 or len(west_ports) % 2 == 1:
            y_size += 1

        # Now generate the cells
        for x_index in range(x_size):
            # Create a new row
            cell_list.append([])
            for y_index in range(y_size):
                # Create a new cell
                cell_list[x_index].append(PrimitiveCell(x_index, y_index, 1, []))

        # Next, generate the different pieces of
        # ports based on their presence and
        # activate/deactivate all the other
        # ports for the component
        #
        #       ------X--
        #       |<-X    |
        #       |       |
        #       |    X->|
        #       --X------
        #
        # Basically, the ports are all pushed to the edges for free with this method

        # Since we have to activate the ports from the center, we need to find the center
        # for the odd and even cases of the composite cell size and the number of ports.
        # Then we need to repeat the process for all the sides

        staging_list = [
            (ComponentSide.NORTH, x_size, north_ports),
            (ComponentSide.EAST, y_size, east_ports),
            (ComponentSide.SOUTH, x_size, south_ports),
            (ComponentSide.WEST, y_size, west_ports),
        ]

        # Now loop through all the sides and activate the ports
        for side, size, ports in staging_list:
            CompositeCell.activate_ports(cell_list, side, size, ports)

            # Spread the ports outwards based on the relative distances
            # between the ports. THRESHOLD doesn't matter here since we
            # aren't yet doing the expansion with spacer blocks
            CompositeCell.spread_ports(
                cell_list=cell_list, side=side, component=component, ports_list=ports
            )

        # Generate 'spacer' blocks with the space
        # modulo THRESHOLD based on inter port
        # distances
        # Generate the spacers for the different sides
        generate_spacers(
            cell_list, top_port_list=north_ports, bottom_port_list=south_ports, is_horizontal=True
        )
        generate_spacers(
            cell_list, top_port_list=east_ports, bottom_port_list=west_ports, is_horizontal=False
        )
        ret = CompositeCell(cell_list)
        return ret

    def print_cell(self):
        """Prints the composite cell"""

        for row in self._cells:
            for cell in row:
                cell.print_cell()
