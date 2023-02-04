from __future__ import annotations
from enum import Enum
from typing import List


class ComponentSide(Enum):
    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"


class PrimitiveCell:

    def __init__(self, x_coord: int, y_coord: int, size: int, ports_exists: List[ComponentSide]):
        """ Initializes a primitive cell with the given size and coordinates

        To initialize this give the x, y relative coordinates in the macro cell. 
        By giving the list of ports that exist on the cell, the ports will 
        be present on the edge of the primitive to form the macro cell.

        Basically everything is setup to be used in unit grid sizes. So it'll let
        you scale stuff however you want. The logic for the sizing should not be done
        manually, utilize the CompositeCell class to do that.

                        ----X----
                        |       |
                        X       X
                        |       |
                        ----X----
        
        Args:
            size (int): Default size of the cell edge
            x_coord (int): the relative x coordinate of the cell in the macro cell
            y_coord (int): the relative y coordinate of the cell in the macro cell
            ports_exists (List[PortSide]): List of which ports exist on the primitive cell
        """
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
        for port in ports_exists:
            if port is ComponentSide.NORTH:
                self._north_port = True
            elif port is ComponentSide.EAST:
                self._east_port = True
            elif port is ComponentSide.SOUTH:
                self._south_port = True
            elif port is ComponentSide.WEST:
                self._west_port = True
    

    @property
    def x_offset(self) -> int:
        """ Returns the x coordinate of the cell

        Returns:
            int: The x coordinate of the cell
        """
        return self._x_coord

    @property
    def y_offset(self) -> int:
        """ Returns the y coordinate of the cell

        Returns:
            int: The y coordinate of the cell
        """
        return self._y_coord
    
    @property
    def dimension(self) -> int:
        """ Returns the dimension of the cell

        Returns:
            int: The dimension of the cell
        """
        return self._dimension
    
    @property
    def north_port(self) -> bool:
        """ Returns the flag for the north port

        Returns:
            bool: The flag for the north port
        """
        return self._north_port
    
    @property
    def east_port(self) -> bool:
        """ Returns the flag for the east port

        Returns:
            bool: The flag for the east port
        """
        return self._east_port
    
    @property
    def south_port(self) -> bool:
        """ Returns the flag for the south port

        Returns:
            bool: The flag for the south port
        """
        return self._south_port
    
    @property
    def west_port(self) -> bool:
        """ Returns the flag for the west port

        Returns:
            bool: The flag for the west port
        """
        return self._west_port

        
    
    def activate_port(self, side: ComponentSide) -> None:
        """ Sets the cell at the given coordinates to active

        Args:
           side (ComponentSide): The side of the composite cell to activate
        """
        if side is ComponentSide.NORTH:
            self._north_port = True
        elif side is ComponentSide.EAST:
            self._east_port = True
        elif side is ComponentSide.SOUTH:
            self._south_port = True
        else:
            self._west_port = True
    
    
    def deactivate_port(self, side: ComponentSide) -> None:
        """ Sets the cell at the given coordinates to deactivate

        Args:
           side (ComponentSide): The side of the composite cell to activate
        """
        if side is ComponentSide.NORTH:
            self._north_port = False
        elif side is ComponentSide.EAST:
            self._east_port = False
        elif side is ComponentSide.SOUTH:
            self._south_port = False
        else:
            self._west_port = False
    
    
    def print_cell(self):
        """ Prints a primitive cell in the following format:

                        ----X----
                        |       |
                        X       X
                        |       |
                        ----X----
        
        
        """
        # Print a box with - and | 5 times on each side with an X in the middle if there is a port
        PORT_INDICATOR = "X"
        WEST_BOUNDARY_INDICATOR = "|"
        EAST_BOUNDARY_INDICATOR = "|"
        NORTH_BOUNDARY_INDICATOR = "-"
        SOUTH_BOUNDARY_INDICATOR = "-"
        
        top_row_string =  NORTH_BOUNDARY_INDICATOR * 4 + (PORT_INDICATOR if self._north_port else NORTH_BOUNDARY_INDICATOR) + NORTH_BOUNDARY_INDICATOR * 4
        bottom_row_string = SOUTH_BOUNDARY_INDICATOR * 4 + (PORT_INDICATOR if self._south_port else SOUTH_BOUNDARY_INDICATOR) + SOUTH_BOUNDARY_INDICATOR * 4
        spacer_row_string = WEST_BOUNDARY_INDICATOR + " " * 7 + EAST_BOUNDARY_INDICATOR
        middle_row_string = (PORT_INDICATOR if self._west_port else WEST_BOUNDARY_INDICATOR) + (" " * 7 ) + (PORT_INDICATOR if self._east_port else EAST_BOUNDARY_INDICATOR)

        print(top_row_string)
        print(spacer_row_string)
        print(middle_row_string)
        print(spacer_row_string)
        print(bottom_row_string)


