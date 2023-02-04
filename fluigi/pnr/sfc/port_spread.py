from typing import Dict, List
from parchmint.component import Component
from parchmint.port import Port
from fluigi.pnr.sfc.primitivecell import ComponentSide
import math



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

