from enum import Enum
from typing import List


class PortExists(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4

class PrimitiveCell:

    def __init__(self, size: int, x_coord: int, y_coord: int, ports: List[PortExists]):
        # Set the coordinates and size of the cell
        self._x_coord = x_coord
        self._y_coord = y_coord
        self._dimension = size

        # Initialize the flags for the ports
        self._east_port = False
        self._west_port = False
        self._north_port = False
        self._south_port = False

        # Go through the list of ports and set the appropriate flags
        for port in ports:
            if port is PortExists.NORTH:
                self._north_port = True
            elif port is PortExists.EAST:
                self._east_port = True
            elif port is PortExists.SOUTH:
                self._south_port = True
            elif port is PortExists.WEST:
                self._west_port = True
        

    def print_cell(self, 
                #    skip_north: bool = False, 
                #    skip_east: bool = False, 
                #    skip_south: bool = False, 
                #    skip_west: bool = False
                   ):
        # Print a box with - and | 5 times on each side with an X in the middle if there is a port
        PORT_INDICATOR = "X"
        WEST_BOUNDARY_INDICATOR = "|"
        EAST_BOUNDARY_INDICATOR = "|"
        NORTH_BOUNDARY_INDICATOR = "-"
        SOUTH_BOUNDARY_INDICATOR = "-"

        # skip_north_east = False
        # skip_north_west = False
        # skip_south_east = False
        # skip_south_west = False

        # if skip_north:
        #     skip_north_east = True
        #     skip_north_west = True
        #     NORTH_BOUNDARY_INDICATOR = " "
        
        # if skip_east:
        #     skip_north_east = True
        #     skip_south_east = True
        #     EAST_BOUNDARY_INDICATOR = " "
        
        # if skip_south:
        #     skip_south_east = True
        #     skip_south_west = True
        #     SOUTH_BOUNDARY_INDICATOR = " "
        
        # if skip_west:
        #     skip_north_west = True
        #     skip_south_west = True
        #     WEST_BOUNDARY_INDICATOR = " "
        
        top_row_string =  NORTH_BOUNDARY_INDICATOR * 3 + (PORT_INDICATOR if self._north_port else NORTH_BOUNDARY_INDICATOR) + NORTH_BOUNDARY_INDICATOR * 3
        bottom_row_string = SOUTH_BOUNDARY_INDICATOR * 3 + (PORT_INDICATOR if self._south_port else SOUTH_BOUNDARY_INDICATOR) + SOUTH_BOUNDARY_INDICATOR * 3
        spacer_row_string = WEST_BOUNDARY_INDICATOR + " " * 5 + EAST_BOUNDARY_INDICATOR
        middle_row_string = (PORT_INDICATOR if self._west_port else WEST_BOUNDARY_INDICATOR) + (" "*5 ) + (PORT_INDICATOR if self._east_port else EAST_BOUNDARY_INDICATOR)

        print(top_row_string)
        print(spacer_row_string)
        print(middle_row_string)
        print(spacer_row_string)
        print(bottom_row_string)

