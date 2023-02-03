from __future__ import annotations
from enum import Enum
from typing import List, Dict, NamedTuple
from parchmint.component import Component
from parchmint.port import Port
from queue import Queue
import math


from fluigi.pnr.sfc.primitivecell import ComponentSide, PrimitiveCell


def get_closest_side(component: Component, port: Port) -> ComponentSide:
    """Returns the closest side to the port

    Args:
        port (Port): The port to find the closest side to

    Returns:
        PortSide: The closest side to the port
    """

    # Get the closest side to the port
    north_distance = port.y
    south_distance = component.yspan - port.y
    east_distance = port.x
    west_distance = component.xspan - port.x

    # Return the closest side
    if north_distance <= min([south_distance, east_distance, west_distance]):
        return ComponentSide.NORTH
    elif east_distance <= min([south_distance, north_distance, west_distance]):
        return ComponentSide.EAST
    elif south_distance <= min([north_distance, east_distance, west_distance]):
        return ComponentSide.SOUTH
    else:
        return ComponentSide.WEST


def try_shift_left(spread_array: List[bool], binning_data: Dict[int, int]):
    # look at the binning for the item
    # of that index see if it needs to
    # go more left. If yes then push it
    # to the left-most feasible point
    for cursor in range(len(spread_array)):
        if spread_array[cursor] is True:
            # Get the bin_location from the binning data
            bin_location = binning_data[cursor]
            # Shift to the furthest point to the left
            # Check if this is a left shift
            if bin_location < cursor:
                # Shift to the furthest point to the left
                shift_furthest_fesible_point(spread_array, cursor, bin_location)
            else:
                # No need to shift
                pass


def try_shift_right(spread_array: List[bool], binning_data: Dict[int, int]):
    # look at the binning for the item
    # of that index see if it needs to
    # go more right. If yes then push it
    # to the left-most feasible point
    for cursor in range(len(spread_array) - 1, -1, -1):
        if spread_array[cursor] is True:
            # Get the bin_location from the binning data
            bin_location = binning_data[cursor]
            # Shift to the furthest point to the left
            # Check if this is a left shift
            if bin_location > cursor:
                # Shift to the furthest point to the left
                shift_furthest_fesible_point(spread_array, cursor, bin_location)
            else:
                # No need to shift
                pass


def generate_bin_map(spread_array, port_list, component, side) -> Dict[int, int]:
    # the bin map has left to right ordered
    # ports with with the positon binned
    bin_map = {}
    for index, port in enumerate(port_list):
        if side is ComponentSide.NORTH or side is ComponentSide.SOUTH:
            # compare for dimension x when generating the map
            bin_map[index] = int(
                math.floor(port.x / component.xspan * len(spread_array))
            )
        else:
            # compare for dimension y when generating the map
            bin_map[index] = int(
                math.floor(port.y / component.yspan * len(spread_array))
            )

    return bin_map


def shift_furthest_fesible_point(array, start_index, target_index):
    # Here the start_index is where the number actually is
    # and the target_index is where the bin_map reckons the
    # the point should be
    found_flag = False

    # If its the same location, retrun without making any changes
    if target_index == start_index:
        return

    elif target_index <= start_index:
        # In the scenario that goes down from target_index --> start_index
        # loop downwards until you see another
        # for cursor=start_index; cursor>=target_index; i=-1:
        for cursor in range(start_index - 1, target_index - 1, -1):
            if array[cursor] == 1:
                # Found the furthest point set to
                # right of furthest point and unset the start point
                array[cursor + 1] = 1
                array[start_index] = 0
                found_flag = True

        if found_flag is False:
            array[target_index] = 1
            array[start_index] = 0

    elif target_index >= start_index:
        # In the scenario that goes up from start_index -> target_index
        # loop downwards until you see another
        # for cursor=start_index; cursor>=target_index; i=+1:
        for cursor in range(start_index + 1, target_index + 1, 1):
            if array[cursor] == 1:
                # Found the furthest point set to
                # left of furthest point and unset the start point
                array[cursor - 1] = 1
                array[start_index] = 0
                found_flag = True

            if found_flag is False:
                array[target_index] = 1
                array[start_index] = 0

    return


class SpacerInsert(NamedTuple):
    """A named tuple that holds the information about a spacer insertion. This structure is
    then used to insert the spacers into the cell list. Since we provide the cooridnate,
    the number of spacers, we prevent the array from mutating.

    We pass the the relative coordinate of the insertion becuase perform the insertions port
    scanning from left to right.

    Additionally, we handle what happens to the ports that are before and after the insertion.
    by clearly defining the status of the ports. Since ther are 4 ports whose fate needs to be
    determined, we keep track of. Here's the example

    [ ][ ][tl][tr][ ][ ][ ]
    [ ][ ][bl][br][ ][ ][ ]

    tl - Top Left (BEFORE | IGNORE | AFTER)
    tr - Top Right (BEFORE | IGNORE | AFTER)
    bl - Bottom Left (BEFORE | IGNORE | AFTER)
    br - Bottom Right (BEFORE | IGNORE | AFTER)

    Attributes:
        relative_insert_coordinate (int): The x or y coordinate of the insertion relative to the previous insertion
        number_of_spacers (int): The number of spacers to insert
        port_topleft_fate (bool): Dictates what happens to the port on the top left
        port_bottomleft_fate (bool): Dictates what happens to the port on the bottom left
        port_topright_fate (bool): Dictates what happens to the port on the top right
        port_bottomright_fate (bool): Dictates what happens to the port on the bottom right
    """

    relative_insert_coordinate: int
    number_of_spacers: int
    port_topleft_fate: bool
    port_bottomleft_fate: bool
    port_topright_fate: bool
    port_bottomright_fate: bool


def insert_horizontal_spacer_column(
    cell_list: List[List[PrimitiveCell]],
    insert_index: int,
    set_north_port: bool = False,
    set_south_port: bool = False,
):
    # Insert a column of spacers at the insert_index
    for row_index, row in enumerate(cell_list):
        row.insert(
            insert_index,
            PrimitiveCell(
                x_coord=insert_index,
                y_coord=row_index,
                size=cell_list[0][0].dimension,
                ports_exists=[],
            ),
        )
    if set_north_port is True:
        # Set the north port of the inserted column's top cell
        cell_list[0][insert_index].activate_port(ComponentSide.NORTH)

    if set_south_port is True:
        # Set the south port of the inserted column's bottom cell
        cell_list[-1][insert_index].activate_port(ComponentSide.SOUTH)


def get_spacer_size(min_dimension: float, max_dimension: float, current_gap: int = 0) -> int:
    # Return 1 for now
    size = 1 - current_gap
    if size < 0:
        return 0
    else :
        return size 



def generate_spacers(
    cell_list: List[List[PrimitiveCell]],
    top_port_list: List[Port],
    bottom_port_list: List[Port],
    is_horizontal: bool = True,
) -> None:
    # Make a copy of the north and south port list so that we can pop from them in the case checking
    north_port_list_fifo: List[Port] = [port for port in top_port_list]
    south_port_list_fifo: List[Port] = [port for port in bottom_port_list]
    attention_array_north = []
    attention_array_south = []
    for index in range(len(cell_list[0])):
        attention_array_north.append(cell_list[0][index].north_port)
        attention_array_south.append(cell_list[-1][index].south_port)

    # Now for the spacer strategy
    # Loop through the attention arrays and at every index, check if there
    # is a port on north and south
    # Case 1:
    # [ ][ ][ ][o][ ][ ][ ]
    # [ ][ ][ ][o][ ][ ][ ]
    # Case 2:
    # Case 2.1:
    # [o][ ][ ][x][ ][ ][ ]
    # [o][ ][ ][ ][ ][ ][ ]
    # Case 2.2:
    # [o][ ][ ][ ][ ][ ][ ]
    # [o][ ][ ][x][ ][ ][ ]
    # Case 3:
    # [ ][x][ ][ ][ ][ ][ ]
    # [ ][ ][x][ ][ ][ ][ ]
    #       OR
    # [ ][ ][ ][x][ ][ ][ ]
    # [ ][ ][x][ ][ ][ ][ ]
    # Case 3.3 (Don't Care):
    # [ ][ ][x][x][ ][ ][ ]
    # [ ][ ][x][ ][ ][ ][ ]
    #       OR
    # [ ][ ][x][ ][ ][ ][ ]
    # [ ][ ][x][x][ ][ ][ ]
    # Case 4:
    # [ ][x][ ][ ][ ][ ][ ]
    # [ ][x][ ][ ][ ][ ][ ]
    # Devolves into the following cases:
    # [ ][ ][ ][x][ ][ ][ ]
    # [ ][ ][x][x][ ][ ][ ]
    #       OR
    # [ ][ ][x][x][ ][ ][ ]
    # [ ][ ][x][ ][ ][ ][ ]
    #       OR
    # [o][x][ ][ ][ ][ ][ ]
    # [o][x][ ][ ][ ][ ][ ]
    # Keep in mind that as we scan we are always going to compare against
    # the previous column's largest x coordinate

    # We check for these cases by doing a scanner going from left to right
    # the scanner will have the memory of the previous column's largest x coordinate
    # so as soon as we see 1 or 2 ports in a column, we can compare against the
    # smallest of the new ports and insert spacers based on the spacer_function.
    # if there are two ports, then after we compare against the previous column's memory,
    # we compare both the ones in the current column and then insert spacers based on the
    # spacer_function again. splitting the north and south ports on either side of the
    # spacer column.

    # Things Scanner Should Keep Track Of
    previous_insert_index = 0
    previous_port_max_coordinate = 0
    current_gap_size = 0

    top_left_ground_truth = False
    bottom_left_ground_truth = False

    # Things to evaulate on the current state
    top_right_ground_truth = False
    bottom_right_ground_truth = False

    current_port_max_coordinate = 0
    current_port_min_coordinate = 0

    def get_port_coordinate(port) -> int:
        if is_horizontal:
            return port.x
        else:
            return port.y

    # All the spacer insertions:
    spacer_insertion_list: List[SpacerInsert] = []

    # Loop through the attention arrays and at every index, and check for insertion
    for scanner_index in range(len(cell_list)):
        # load the status of the ports into the ground truth variables (right)
        if is_horizontal: # TODO- Add case for vertical
            top_right_ground_truth = cell_list[0][scanner_index].north_port
            bottom_right_ground_truth = cell_list[-1][scanner_index].south_port
        else:
            top_right_ground_truth = cell_list[0][scanner_index].west_port
            bottom_right_ground_truth = cell_list[-1][scanner_index].east_port

        # Load the next set of ports and the do the comparison
        top_right_port = None
        bottom_right_port = None
        if top_right_ground_truth is True:
            try:
                top_right_port = north_port_list_fifo.pop(0)
            except IndexError:
                raise IndexError(
                    "North Port List is empty, but there is a port in the cell list"
                )

        if bottom_right_ground_truth is True:
            try:
                bottom_right_port = south_port_list_fifo.pop(0)
            except IndexError:
                raise IndexError(
                    "South Port List is empty, but there is a port in the cell list"
                )

        # Set the min/max port sides and coordinates if both ports exist
        if top_right_ground_truth is True and bottom_right_ground_truth is False:

            # Check to make sure we have the port data
            if top_right_port is None:
                raise ValueError("Top right port is None")
            current_port_max_coordinate = get_port_coordinate(top_right_port)
            current_port_min_coordinate = get_port_coordinate(top_right_port)
        elif top_right_ground_truth is False and bottom_right_ground_truth is True:

            # Check to make sure we have the port data
            if bottom_right_port is None:
                raise ValueError("Bottom right port is None")
            current_port_max_coordinate = get_port_coordinate(bottom_right_port)
            current_port_min_coordinate = get_port_coordinate(bottom_right_port)
        elif top_right_ground_truth is True and bottom_right_ground_truth is True:

            # Check to make sure we have the port data
            if top_right_port is None:
                raise ValueError("Top right port is None")
            if bottom_right_port is None:
                raise ValueError("Bottom right port is None")

            if top_right_port.x > bottom_right_port.x:
                current_port_max_coordinate = get_port_coordinate(top_right_port)
                current_port_min_coordinate = get_port_coordinate(bottom_right_port)
            else:
                current_port_max_coordinate = get_port_coordinate(bottom_right_port)
                current_port_min_coordinate = get_port_coordinate(top_right_port)

        # Rewrite the cases
        # Case 1:
        # [ ][ ][ ][o][ ][ ][ ]
        # [ ][ ][ ][o][ ][ ][ ]
        # This is the case where we just increse the current gap size and
        # continue the scanner
        if top_right_ground_truth is False and bottom_right_ground_truth is False:
            current_gap_size += 1
            continue

        # Case 2: This is what we might see in the beginning of the scanning
        # Case 2.1:
        # [o][ ][ ][x][ ][ ][ ]
        # [o][ ][ ][ ][ ][ ][ ]
        # Case 2.2:
        # [o][ ][ ][ ][ ][ ][ ]
        # [o][ ][ ][x][ ][ ][ ]
        elif (
            # Case 2.1:
            top_right_ground_truth is True
            and bottom_right_ground_truth is False
            and top_left_ground_truth is False
            and bottom_left_ground_truth is False
        ):
            # Do not create a spacer !

            # Update the state information
            previous_port_max_coordinate = get_port_coordinate(top_right_port)
            top_left_ground_truth = True
            bottom_left_ground_truth = False
            current_gap_size += 1

        elif (
            # Case 2.2:
            top_right_ground_truth is False
            and bottom_right_ground_truth is True
            and top_left_ground_truth is False
            and bottom_left_ground_truth is False
        ):
            # Do not create a spacer !

            # Update the state information
            previous_port_max_coordinate = get_port_coordinate(bottom_right_port)
            top_left_ground_truth = False
            bottom_left_ground_truth = True
            current_gap_size += 1

        # Case 3: This is the state that will be the workhorse
        # [ ][x][ ][ ][ ][ ][ ]
        # [ ][ ][x][ ][ ][ ][ ]
        #       OR
        # [ ][ ][ ][x][ ][ ][ ]
        # [ ][ ][x][ ][ ][ ][ ]
        elif (
            # Case 3.1:
            # [ ][x][ ][ ][ ][ ][ ]
            # [ ][ ][x][ ][ ][ ][ ]
            top_right_ground_truth is True
            and bottom_right_ground_truth is False
            and top_left_ground_truth is True
            and bottom_left_ground_truth is False
        ):
            # Generate all the spacer information from the state
            spacer_size = get_spacer_size(previous_port_max_coordinate, current_port_min_coordinate, current_gap_size)
            # Create the spacer insertion
            # Fates:
            #    Top Left    [T][F]   Top Right
            #    Bottom Left [F][T]   Bottom Right
            if spacer_size > 0:
                new_spacer_insertion = SpacerInsert(
                    relative_insert_coordinate=scanner_index - previous_insert_index,
                    number_of_spacers=spacer_size,
                    port_topleft_fate=top_left_ground_truth,
                    port_bottomleft_fate=bottom_left_ground_truth,
                    port_topright_fate=top_right_ground_truth,
                    port_bottomright_fate=bottom_right_ground_truth,
                )
                spacer_insertion_list.append(new_spacer_insertion)
            # Update the state information
            previous_port_max_coordinate = current_port_max_coordinate
            previous_insert_index = scanner_index
            current_gap_size = 0
            top_left_ground_truth = True
            bottom_left_ground_truth = False
        elif (
            # Case 3.2:
            # [ ][ ][ ][x][ ][ ][ ]
            # [ ][ ][x][ ][ ][ ][ ]
            top_right_ground_truth is False
            and bottom_right_ground_truth is True
            and top_left_ground_truth is False
            and bottom_left_ground_truth is True
        ):
            # Generate all the spacer information from the state
            spacer_size = get_spacer_size(previous_port_max_coordinate, current_port_min_coordinate, current_gap_size)
            # Create the spacer insertion
            # Fates:
            #    Top Left    [F][T]   Top Right
            #    Bottom Left [T][F]   Bottom Right
            if spacer_size > 0:
                new_spacer_insertion = SpacerInsert(
                    relative_insert_coordinate=scanner_index - previous_insert_index,
                    number_of_spacers=spacer_size,
                    port_topleft_fate=top_left_ground_truth,
                    port_bottomleft_fate=bottom_left_ground_truth,
                    port_topright_fate=top_right_ground_truth,
                    port_bottomright_fate=bottom_right_ground_truth,
                )
                spacer_insertion_list.append(new_spacer_insertion)
            # Update the state information
            previous_port_max_coordinate = current_port_max_coordinate
            previous_insert_index = scanner_index
            current_gap_size = 0
            top_left_ground_truth = False
            bottom_left_ground_truth = True

        elif (
            # Case 3.3:
            top_left_ground_truth is True
            and bottom_left_ground_truth is True
        ):
            # Do Both the above cases
            # Generate all the spacer information from the state
            spacer_size = get_spacer_size(previous_port_max_coordinate, current_port_min_coordinate, current_gap_size)
            # Create the spacer insertion
            # Fates:
            #    Top Left    [T][F]   Top Right
            #    Bottom Left [T][T]   Bottom Right
            # OR:
            #    Top Left    [T][T]   Top Right
            #    Bottom Left [T][F]   Bottom Right
            if spacer_size > 0:
                new_spacer_insertion = SpacerInsert(
                    relative_insert_coordinate=scanner_index - previous_insert_index,
                    number_of_spacers=spacer_size,
                    port_topleft_fate=top_left_ground_truth,
                    port_bottomleft_fate=bottom_left_ground_truth,
                    port_topright_fate=top_right_ground_truth,
                    port_bottomright_fate=bottom_right_ground_truth,
                )
                spacer_insertion_list.append(new_spacer_insertion)
            # Update the state information
            previous_port_max_coordinate = current_port_max_coordinate
            previous_insert_index = scanner_index
            current_gap_size = 0
            top_left_ground_truth = True
            bottom_left_ground_truth = True

        # Case 4:
        # [ ][x][ ][ ][ ][ ][ ]
        # [ ][x][ ][ ][ ][ ][ ]
        # Devolves into the following cases:
        # [o][x][ ][ ][ ][ ][ ]
        # [o][x][ ][ ][ ][ ][ ]
        #       OR
        # [ ][ ][x][x][ ][ ][ ]
        # [ ][ ][x][ ][ ][ ][ ]
        #       OR
        # [ ][ ][ ][x][ ][ ][ ]
        # [ ][ ][x][x][ ][ ][ ]
        # Step 4.1: Insert spacers for the previous columns
        # Step 4.2: Insert spacers for the current column
        elif top_right_ground_truth is True and bottom_right_ground_truth is True:
            # Since we have two steps for this process, we need to check the 3
            # Subcases for the first step
            if (
                # Case 4.1.1:
                # [o][x][ ][ ][ ][ ][ ]
                # [o][x][ ][ ][ ][ ][ ]
                top_right_ground_truth is True
                and bottom_right_ground_truth is True
                and top_left_ground_truth is False
                and bottom_left_ground_truth is False
            ):
                # Do not create the spacer insertion / This is the first insert in the sequence
                # Update the state information
                current_gap_size = 0
                # Do not update previous_port_max_coordinate and left* ground truths

            elif (
                # Case 4.1.2:
                # [ ][ ][x][x][ ][ ][ ]
                # [ ][ ][x][ ][ ][ ][ ]
                top_right_ground_truth is True
                and bottom_right_ground_truth is True
                and bottom_left_ground_truth is True
                and top_left_ground_truth is False
            ):
                # Generate all the spacer information from the state
                pass
                spacer_size = get_spacer_size(previous_port_max_coordinate, current_port_min_coordinate, current_gap_size)
                # Create the spacer insertion
                # Fates:
                #    Top Left    [T][T]   Top Right
                #    Bottom Left [T][F]   Bottom Right
                if spacer_size > 0:
                    new_spacer_insertion = SpacerInsert(
                        relative_insert_coordinate=scanner_index - previous_insert_index,
                        number_of_spacers=spacer_size,
                        port_topleft_fate=top_left_ground_truth,
                        port_bottomleft_fate=bottom_left_ground_truth,
                        port_topright_fate=top_right_ground_truth,
                        port_bottomright_fate=bottom_right_ground_truth,
                    )
                    spacer_insertion_list.append(new_spacer_insertion)
                # Update the state information
                previous_insert_index = scanner_index
                current_gap_size = 0
                # Do not update previous_port_max_coordinate and left* ground truths

            elif (
                # Case 4.1.3:
                # [ ][ ][ ][x][ ][ ][ ]
                # [ ][ ][x][x][ ][ ][ ]
                top_right_ground_truth is True
                and bottom_right_ground_truth is True
                and top_left_ground_truth is False
                and bottom_left_ground_truth is True
            ):
                # Generate all the spacer information from the state
                pass
                spacer_size = get_spacer_size(previous_port_max_coordinate, current_port_min_coordinate, current_gap_size)
                # Create the spacer insertion
                # Fates:
                #    Top Left    [F][T]   Top Right
                #    Bottom Left [T][T]   Bottom Right
                if spacer_size > 0:
                    new_spacer_insertion = SpacerInsert(
                        relative_insert_coordinate=scanner_index - previous_insert_index,
                        number_of_spacers=spacer_size,
                        port_topleft_fate=top_left_ground_truth,
                        port_bottomleft_fate=bottom_left_ground_truth,
                        port_topright_fate=top_right_ground_truth,
                        port_bottomright_fate=bottom_right_ground_truth,
                    )
                    spacer_insertion_list.append(new_spacer_insertion)
                # Update the state information
                previous_insert_index = scanner_index
                current_gap_size = 0
                # Do not update previous_port_max_coordinate and left* ground truths

            # Step 4.2: Insert spacers for the current column
            # Skip if the top and bottom are the same x coordinate
            spacer_size = get_spacer_size(
                get_port_coordinate(top_right_port),
                get_port_coordinate(bottom_right_port),
                current_gap_size
            )
            if  spacer_size == 0 :
                # Update the state information
                previous_port_max_coordinate = current_port_max_coordinate
                top_left_ground_truth = True
                bottom_left_ground_truth = True
                current_gap_size = 0

                # We dont do any more changes becuase we end up having both top and bottom at the same level

            else:
                # Generate all the spacer information from the state
                # Comparing the top and bottom ports to determine the fate of the left ports after the inplace insert
                # [][][][x][][][][]
                # [][][][x][][][][]
                if get_port_coordinate(top_right_port) > get_port_coordinate(bottom_right_port):
                    # Fates:
                    #    Top Left    [F][T]   Top Right
                    #    Bottom Left [T][F]   Bottom Right
                    top_right_fate = True
                    bottom_right_fate = False
                    top_left_fate = False
                    bottom_left_fate = True
                else:
                    # Fates:
                    #    Top Left    [T][F]   Top Right
                    #    Bottom Left [F][T]   Bottom Right
                    top_right_fate = False
                    bottom_right_fate = True
                    top_left_fate = True
                    bottom_left_fate = False
                spacer_size = get_spacer_size(
                    get_port_coordinate(top_right_port), 
                    get_port_coordinate(bottom_right_port), 
                    current_gap_size
                )
                # Create the spacer insertion
                if spacer_size > 0:
                    new_spacer_insertion = SpacerInsert(
                        relative_insert_coordinate=scanner_index - previous_insert_index,
                        number_of_spacers=spacer_size,
                        port_topleft_fate=top_left_fate,
                        port_bottomleft_fate=bottom_left_fate,
                        port_topright_fate=top_right_fate,
                        port_bottomright_fate=bottom_right_fate,
                    )
                    spacer_insertion_list.append(new_spacer_insertion)
                # Update the state information
                previous_insert_index = scanner_index
                current_gap_size = 0
                previous_port_max_coordinate = current_port_max_coordinate
                bottom_left_ground_truth = bottom_right_fate
                top_left_ground_truth = top_right_fate

        else:
            raise ValueError("Invalid state Encountered, need to fix algorithm logic")


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
