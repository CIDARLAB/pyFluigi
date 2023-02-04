import math
from typing import Dict, List

from parchmint.component import Component
from parchmint.port import Port

from fluigi.pnr.sfc.primitivecell import ComponentSide


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


def generate_bin_map(spread_array: List[bool], port_list: List[Port], component: Component, side: ComponentSide) -> Dict[int, int]:
    """ Generate the bin map for the ports, basically bins the coordinates of the ports to locations on the spread array
    which is a boolean array representing the side of the component. The bin map is a dictionary with the index of the
    port in the port list as the key and the ideal spread array location as the value.


    Args:
        spread_array (List[bool]): Spread array representing the side of the component
        port_list (List[Port]): List of ports on the component for the given side
        component (Component): Component object
        side (ComponentSide): Side of the component for which the ports are being binned used to determine the co-ordinate to bin

    Returns:
        Dict[int, int]: Dictionary with the index of the port in the port list as the key and the ideal spread array location as the value
    """
    # the bin map has left to right ordered
    # ports with with the positon binned
    bin_map = {}
    for index, port in enumerate(port_list):
        if side is ComponentSide.NORTH or side is ComponentSide.SOUTH:
            # compare for dimension x when generating the map
            coordinate = port.x
        else:
            # compare for dimension y when generating the map
            coordinate = port.y
        
        location = int(
            math.floor(coordinate/ component.xspan * len(spread_array))
        )

        # check if the location is size of the spread 
        # array (when its an integer overflow)
        if location == len(spread_array):
            location = len(spread_array) - 1
        
        bin_map[index] = location


    return bin_map


def shift_furthest_fesible_point(array: List[bool], start_index: int, target_index: int) -> None:
    """ Shift the furthest feasible point to the left or right of the start_index
    closest to the target_index. This is done by looking at the array and finding
    the furthest point to the left or right of the start_index and then shifting
    it.

    Args:
        array (List[bool]): Spread array representing the side of the component
        start_index (int): start_index is the index of the point that needs to be shifted
        target_index (int): target_index is the index of the point to which the start_index needs to be shifted
    """

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
            if array[cursor] == True:
                # Found the furthest point set to
                # right of furthest point and unset the start point
                array[cursor + 1] = True
                array[start_index] = False
                found_flag = True

        if found_flag is False:
            array[target_index] = True
            array[start_index] = False

    elif target_index >= start_index:
        # In the scenario that goes up from start_index -> target_index
        # loop downwards until you see another
        # for cursor=start_index; cursor>=target_index; i=+1:
        for cursor in range(start_index + 1, target_index + 1, 1):
            if array[cursor] == True:
                # Found the furthest point set to
                # left of furthest point and unset the start point
                array[cursor - 1] = True
                array[start_index] = False
                found_flag = True

            if found_flag is False:
                array[target_index] = True
                array[start_index] = False

    return

