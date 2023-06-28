from __future__ import annotations

from typing import Dict, List, NamedTuple

from parchmint.component import Component
from parchmint.port import Port

from fluigi.parameters import SPACER_THRESHOLD
from fluigi.pnr.sfc.port_spread import spread_ports
from fluigi.pnr.sfc.primitivecell import ComponentSide, PrimitiveCell
from fluigi.pnr.sfc.spacer_insert import generate_spacers
from fluigi.pnr.sfc.utils import get_closest_side


class CompositeCell:
    def __init__(self, cell_list: List[List[PrimitiveCell]]) -> None:
        """Initializes the composite cell

        Args:
            cell_list (List[List[PrimitiveCell]]): List of lists of primitive cells that make up the composite cell

        Raises:
            ValueError: If the cell list is empty / the coordinates of the cells are incorrect
        """
        # Check to ensure all primitive cell indexes are correct
        for row_index, _ in enumerate(cell_list):
            for column_index, item in enumerate(cell_list[row_index]):
                temp_cell = item
                if (temp_cell.y_offset, temp_cell.x_offset) != (row_index, column_index):
                    raise ValueError(
                        f"Cell at index ({temp_cell.y_offset}, {temp_cell.x_offset}) has an incorrect index of {item}"
                    )

        self._cells = cell_list

    def get_cell(self, x: int, y: int) -> PrimitiveCell:
        """Returns the cell at the given coordinates

        Args:
            x (int): x coordinate of the cell
            y (int): y coordinate of the cell

        Returns:
            PrimiveCell: The cell at the given coordinates
        """
        return self._cells[y][x]

    def rotate_clockwise(self) -> None:
        """Rotates the composite cell clockwise (90 degrees)

        Regenerates the cell_list completely and activates the ports accordingly
        """
        # Move the reference to a backup variable
        # Create a new list of lists
        # The rows become the columns and the column become the rows
        # All the individual ports also need to be rotated i.e. any port that has
        # NORTH -> EAST
        # EAST -> SOUTH
        # SOUTH -> WEST
        # WEST -> NORTH

        # Create a new list of lists
        backup_cells_list = self._cells
        blueprint_cell = backup_cells_list[0][0]
        # Get the dimensions of the list
        rows = len(backup_cells_list)
        columns = len(backup_cells_list[0])
        # Create a new list of lists
        new_rows = columns
        new_columns = rows

        # Create a new list of lists
        cell_list = []
        # Now generate the cells
        for y_index in range(new_rows):
            # Create a new row
            cell_list.append([])
            for x_index in range(new_columns):
                # Create a new cell
                cell_list[y_index].append(PrimitiveCell(x_index, y_index, blueprint_cell.dimension, []))

        # Generate a boolean array for the N, E, S, W sides
        north_side = [cell.north_port for cell in backup_cells_list[0]]
        south_side = [cell.south_port for cell in backup_cells_list[-1]]
        east_side = [cell.east_port for cell in [row[-1] for row in backup_cells_list]]
        west_side = [cell.west_port for cell in [row[0] for row in backup_cells_list]]

        # Activate the east ports in the new cell list by looking at the north side of the old cell list
        for index, item in enumerate(north_side):
            # Check if true on the north side
            if item:
                cell_list[index][-1].activate_port(ComponentSide.EAST)

        # Activate the south ports in the new cell list by looking at the east side of the old cell list
        for index, item in enumerate(east_side):
            # Check if true on the east side
            if item:
                cell_list[-1][index].activate_port(ComponentSide.SOUTH)

        # Activate the west ports in the new cell list by looking at the south side of the old cell list
        for index, item in enumerate(south_side):
            # Check if true on the south side
            if item:
                cell_list[index][0].activate_port(ComponentSide.WEST)

        # Activate the north ports in the new cell list by looking at the west side of the old cell list
        for index, item in enumerate(west_side):
            # Check if true on the west side
            if item:
                cell_list[0][index].activate_port(ComponentSide.NORTH)

        # Assign the new cell list to the property
        self._cells = cell_list

    def __eq__(self, o: object) -> bool:
        if isinstance(o, CompositeCell):
            # Check if types are correct
            if len(self._cells) == len(o.cells):
                # Check if the dimensions are the same
                for i, item in enumerate(self._cells):
                    if len(item) != len(o.cells[i]):
                        return False
                # Check if the cells are the same
                for i, item in enumerate(self._cells):
                    for j in range(len(item)):
                        if self.get_cell(j, i) != o.get_cell(j, i):
                            print(f"Cell at ({i}, {j}) is not the same")
                            return False

                # If we get here, then the cells are the same
                return True
            else:
                return False
        else:
            return False

    @property
    def cells(self) -> List[List[PrimitiveCell]]:
        """Returns the cells in the composite cell

        Returns:
            List[List[PrimitiveCell]]: The cells in the composite cell
        """
        return self._cells

    def activate_port(self, x: int, y: int, side: ComponentSide) -> None:
        """Activates a port on the composite cell

        Args:
            x (int): x coordinate of the port.
            y (int): y coordinate of the port.
            side (ComponentSide): side of the port.
        """
        self._cells[y][x].activate_port(side)

    @staticmethod
    def initialize_ports(
        cell_list: List[List[PrimitiveCell]],
        side: ComponentSide,
        ports_list: List[Port],
    ) -> None:
        """Activates the ports on a cell list

        Args:
            cell_list (List[List[PrimitiveCell]]): cell list thats being activated
            side (ComponentSide): side of the composite cell that the ports are on
            size (int): size of the composite cell
            ports_list (List[Port]): list of ports that are being activated

        Raises:
            Exception: If the size is even and the number of ports is odd
        """
        # First figure the size of the composite cell so that we know which index we have to loop
        # through to activate the ports
        is_vertical = False
        size = len(cell_list[0])
        change_index = 0
        if side is ComponentSide.EAST:
            is_vertical = True
            size = len(cell_list)
            change_index = -1
        if side is ComponentSide.WEST:
            is_vertical = True
            size = len(cell_list)
        if side is ComponentSide.SOUTH:
            change_index = -1

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
                for offset in range(0, len(ports_list) // 2 + 1):
                    cell_list[center + offset][change_index].activate_port(side)
                    cell_list[center - offset][change_index].activate_port(side)
            else:
                for offset in range(0, len(ports_list) // 2 + 1):
                    cell_list[change_index][center + offset].activate_port(side)
                    cell_list[change_index][center - offset].activate_port(side)

        # Case 2
        elif size % 2 == 1 and len(ports_list) % 2 == 0:
            # Even number of ports and odd size of composite cell
            #     o     o
            # [ ][ ][ ][ ][ ]
            # Activate the ports
            if is_vertical:
                for offset in range(1, len(ports_list) // 2 + 1):
                    cell_list[center + offset][change_index].activate_port(side)
                    cell_list[center - offset][change_index].activate_port(side)
            else:
                for offset in range(1, len(ports_list) // 2 + 1):
                    cell_list[change_index][center + offset].activate_port(side)
                    cell_list[change_index][center - offset].activate_port(side)

        # Case 4
        elif size % 2 == 0 and len(ports_list) % 2 == 0:
            # Even number of ports and even size of composite cell
            #     o  o
            # [ ][ ][ ][ ]
            # Activate the ports
            if is_vertical:
                for offset in range(0, len(ports_list) // 2):
                    cell_list[center + offset][change_index].activate_port(side)
                    cell_list[center - offset - 1][change_index].activate_port(side)
            else:
                for offset in range(0, len(ports_list) // 2):
                    cell_list[change_index][center + offset].activate_port(side)
                    cell_list[change_index][center - offset - 1].activate_port(side)

        else:  # Case 3
            # Odd number of ports and even size of composite cell
            # Not applicatble since we avoid this scenario
            raise ValueError("Odd number of ports and even size of composite cell is not applicable")

    @staticmethod
    def from_parchmint_component(
        component: Component, spread_ports_enabled: bool = True, insert_spacers_enabled: bool = True
    ) -> CompositeCell:
        """Generates a composite cell from a component

        Args:
            component (Component): Component to generate the composite cell from

        Returns:
            CompositeCell: Composite cell generated from the component
        """
        # TODO - Figure out if this the right way to do this.
        # Currently setting the dimension to be the threshold /
        # We should change the spacer function to be a relaxer
        # eveywhere
        computed_dimension = SPACER_THRESHOLD

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
            elif closest_side is ComponentSide.WEST:
                west_ports.append(port)
            else:
                north_ports.append(port)
                east_ports.append(port)
                south_ports.append(port)
                west_ports.append(port)

        # Now sort the ports based on their x and y coordinates.
        # West->East and South->North
        north_ports.sort(key=lambda port: port.x)
        east_ports.sort(key=lambda port: port.y)
        south_ports.sort(key=lambda port: port.x)
        west_ports.sort(key=lambda port: port.y)

        # horizontal and vertical side port lists to be used for spacer generation in the end
        horizontal_side_port_lists = list(north_ports)
        horizontal_side_port_lists.extend([port for port in south_ports if port not in horizontal_side_port_lists])

        vertical_side_port_lists = list(east_ports)
        vertical_side_port_lists.extend([port for port in west_ports if port not in vertical_side_port_lists])

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

        # Now check if the the ports are odd and the size is even
        if (len(north_ports) % 2 == 1 or len(south_ports) % 2 == 1) and x_size % 2 == 0:
            x_size += 1
        if (len(east_ports) % 2 == 1 or len(west_ports) % 2 == 1) and y_size % 2 == 0:
            y_size += 1

        # Now generate the cells
        for y_index in range(y_size):
            # Create a new row
            cell_list.append([])
            for x_index in range(x_size):
                # Create a new cell
                cell_list[y_index].append(PrimitiveCell(x_index, y_index, computed_dimension, []))

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
            (ComponentSide.NORTH, north_ports),
            (ComponentSide.EAST, east_ports),
            (ComponentSide.SOUTH, south_ports),
            (ComponentSide.WEST, west_ports),
        ]

        # Now loop through all the sides and activate the ports
        for side, ports in staging_list:
            CompositeCell.initialize_ports(cell_list, side, ports)

            if spread_ports_enabled:
                # Spread the ports outwards based on the relative distances
                # between the ports. THRESHOLD doesn't matter here since we
                # aren't yet doing the expansion with spacer blocks
                spread_ports(cell_list=cell_list, side=side, component=component, ports_list=ports)

        if insert_spacers_enabled:
            # Generate 'spacer' blocks with the space
            # modulo THRESHOLD based on inter port
            # distances
            # Generate the spacers for the different sides
            generate_spacers(cell_list, top_port_list=north_ports, bottom_port_list=south_ports, is_horizontal=True)
            generate_spacers(cell_list, top_port_list=east_ports, bottom_port_list=west_ports, is_horizontal=False)

        ret = CompositeCell(cell_list)
        return ret

    def print_cell(self):
        """Prints the composite cell"""
        for row in self._cells:
            top_row_string_full_row = ""
            spacer_row_string_full_row = ""
            middle_row_string_full_row = ""
            bottom_row_string_full_row = ""

            for cell in row:
                # Get the strings for the cell
                top_row_string, spacer_row_string, middle_row_string, bottom_row_string = cell.get_figure()
                # Add the strings to the full row strings
                top_row_string_full_row += top_row_string
                spacer_row_string_full_row += spacer_row_string
                middle_row_string_full_row += middle_row_string
                bottom_row_string_full_row += bottom_row_string

                # Print the full row strings
            print(top_row_string_full_row)
            print(spacer_row_string_full_row)
            print(middle_row_string_full_row)
            print(spacer_row_string_full_row)
            print(bottom_row_string_full_row)

    def print_cell_indexes(self):
        """Prints the composite cell indexes"""
        for row in self._cells:
            row_str = ""
            for cell in row:
                row_str += f"({cell.x_offset}, {cell.y_offset})"
            print(row_str)
