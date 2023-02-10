from typing import List, NamedTuple

from parchmint.port import Port

from fluigi.parameters import SPACER_THRESHOLD
from fluigi.pnr.sfc.primitivecell import ComponentSide, PrimitiveCell


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
    spacer_insert: SpacerInsert,
) -> None:
    """Inserts a column of spacers into the cell list. The column is inserted at the insert_index

    Note: This fuction ignores the relative_insert_coordinate of the spacer_insert, it uses the insert_index
    to insert the column of spacers as the absolute coordinate.

    Args:
        cell_list (List[List[PrimitiveCell]]): Cell list to insert the spacers into
        insert_index (int): The absolute y coordinate of the insertion
        spacer_insert (SpacerInsert): The spacer insert object that holds the information about the insertion
    """    
    # Extract the port setting information from the spacer insert
    #  [ ][ ][BW][AW][ ][ ][ ]
    #  [ ][ ][BE][AE][ ][ ][ ]
    set_before_west_port: bool = spacer_insert.port_topleft_fate
    set_after_west_port: bool = spacer_insert.port_bottomleft_fate
    set_before_east_port: bool = spacer_insert.port_topright_fate
    set_after_east_port: bool = spacer_insert.port_bottomright_fate

    # Insert n Rows of spacers at the insert_index
    for new_index in range(spacer_insert.number_of_spacers):
        new_row = []
        for row_index, row in enumerate(cell_list):
            new_row.insert(
                insert_index,
                PrimitiveCell(
                    x_coord=insert_index + new_index +1,
                    y_coord=row_index,
                    size=cell_list[0][0].dimension,
                    ports_exists=[],
                ),
            )
        cell_list.insert(insert_index + new_index + 1, new_row)

    if  set_before_west_port is True:
        # Set the west port of the inserted column's left cell
        cell_list[insert_index][0].activate_port(ComponentSide.WEST)

    if set_before_west_port is True:
        # Set the east port of the inserted column's right cell
        cell_list[insert_index][-1].activate_port(ComponentSide.EAST)
    
    if set_after_west_port is True:
        # Set the west port of the inserted column's left cell
        cell_list[insert_index + spacer_insert.number_of_spacers+ 1][0].activate_port(ComponentSide.WEST)
    
    if set_after_east_port is True:
        # Set the east port of the inserted column's right cell
        cell_list[insert_index + spacer_insert.number_of_spacers+ 1][-1].activate_port(ComponentSide.EAST)


def insert_vertical_spacer_column(
    cell_list: List[List[PrimitiveCell]],
    insert_index: int,
    set_north_port: bool = False,
    set_south_port: bool = False,
) -> None:
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
    gap = max_dimension - min_dimension
    if gap < SPACER_THRESHOLD:
        return 0
    # Return 1 for now
    size = gap // SPACER_THRESHOLD
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

