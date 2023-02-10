import pytest
from parchmint.port import Port

from fluigi.pnr.sfc.port_spread import generate_bin_map, shift_furthest_fesible_point, try_shift_left, try_shift_right
from fluigi.pnr.sfc.primitivecell import ComponentSide


@pytest.fixture
def north_ports():
    # Create 4 ports in the north side
    port_north_0 = Port("north_0",x=0, y=0)
    port_north_1 = Port("north_1",x=250, y=0)
    port_north_2 = Port("north_2",x=500, y=0)
    port_north_3 = Port("north_3",x=750, y=0)
    port_north_4 = Port("north_4",x=1000, y=0)

    return [port_north_0, port_north_1, port_north_2, port_north_3, port_north_4]


@pytest.fixture
def east_ports():
    # Create 4 ports in the north side
    port_east_0 = Port("east_0",x=1000, y=0)
    port_east_1 = Port("east_1",x=1000, y=250)
    port_east_2 = Port("east_2",x=1000, y=500)
    port_east_3 = Port("east_3",x=1000, y=750)
    port_east_4 = Port("east_4",x=1000, y=1000)

    return [port_east_0, port_east_1, port_east_2, port_east_3, port_east_4]


def test_try_shift_left():
    # Create a spread array of 10 with 0, 4 and 9 as True
    spread_array = [True, False, False, False, True, False, False, False, True]
    binning_data = {0: 0, 1: 4, 2: 8}
    try_shift_left(spread_array, binning_data)

    # nothing should change
    assert spread_array == [True, False, False, False, True, False, False, False, True]

    # Create a spread array of 10 with 3, 4 and 5 as True
    spread_array = [False, False, False, True, True, True, False, False, False]
    binning_data = {0: 0, 1: 4, 2: 8}
    try_shift_left(spread_array, binning_data)

    # Everything to the left of 3 should shift to the left
    assert spread_array == [True, False, False, False, True, True, False, False, False]

    # Create a spread array of 10 with 3, 4, 5, 8 as True
    spread_array = [True, False, False, True, True, True, False, False, False]
    binning_data = {0: 0, 1:0, 2: 4, 3: 8}
    try_shift_left(spread_array, binning_data)
    
    # Everything to the right of 4 should shift to the left
    assert spread_array == [True, True, False, False, True, True, False, False, False]


def test_try_shift_right():
    # Create a spread array of 10 with 0, 4 and 9 as True
    spread_array = [True, False, False, False, True, False, False, False, True]
    binning_data = {0: 0, 1: 4, 2: 8}
    try_shift_right(spread_array, binning_data)

    # nothing should change
    assert spread_array == [True, False, False, False, True, False, False, False, True]

    # Create a spread array of 10 with 3, 4 and 5 as True
    spread_array = [False, False, False, True, True, True, False, False, False]
    binning_data = {0: 0, 1: 4, 2: 8}
    try_shift_right(spread_array, binning_data)

    # Everything to the right of 4 should shift to the Right
    assert spread_array == [False, False, False, True, True, False, False, False, True]

    # Create a spread array of 10 with 3, 4, 5, 8 as True
    spread_array = [False, False, False, True, True, True, False, False, True]
    binning_data = {0: 0, 1: 4, 2: 8, 3: 8}
    try_shift_right(spread_array, binning_data)
    
    # Everything to the right of 4 should shift to the left
    assert spread_array == [False, False, False, True, True, False, False, True, True]




def test_generate_bin_map(north_ports, east_ports, component):
    # Test the bin map generation for the north ports
    # For different kinds of spread arrays
    
    # This is a 10 spread array
    spread_array = [True, True, True, True, True, True, True, True, True, True]
    bin_map = generate_bin_map(spread_array, north_ports, component, ComponentSide.NORTH)
    assert bin_map == {0: 0, 1: 2, 2: 5, 3: 7, 4: 9}

    # This is a 5 spread array
    spread_array = [True, True, True, True, True, True]
    bin_map = generate_bin_map(spread_array, north_ports, component, ComponentSide.NORTH)
    assert bin_map == {0: 0, 1: 1, 2: 3, 3: 4, 4: 5}

    # # Test the same distribution for the east ports
    # spread_array = [True, True, True, True, True, True, True, True, True, True]
    # bin_map = generate_bin_map(spread_array, east_ports, component, ComponentSide.EAST)
    # assert bin_map == {0: 2, 1: 5, 2: 7, 3: 10}

    # # This is a 5 spread array
    # spread_array = [True, True, True, True, True, True]
    # bin_map = generate_bin_map(spread_array, east_ports, component, ComponentSide.EAST)
    # assert bin_map == {0: 1, 1: 3, 2: 4, 3: 5}



def test_shift_furthest_fesible_point():
    # Checkt to make sure that it raises a Value Error if the start index is False
    with pytest.raises(ValueError):
        spread_array = [False, False, True, False, False, False, False, False, False, True]
        shift_furthest_fesible_point(spread_array, 0, 9)

    # Check to make sure that the same index for start and taget make no changes to the array
    spread_array = [False, False, True, False, False, False, False, False, False, True]
    shift_furthest_fesible_point(spread_array, 2, 2)

    # Create a spread array with only 1 true value
    spread_array = [False, False, True, False, False, False, False, False, False, True]
    shift_furthest_fesible_point(spread_array, 2, 9)
    assert spread_array == [False, False, False, False, False, False, False, False, True, True]

    # Create a spread array with only 1 true value
    spread_array = [True, False, True, False, False, False, False, False, False, True]
    shift_furthest_fesible_point(spread_array, 0, 9)
    assert spread_array == [False, True, True, False, False, False, False, False, False, True]

    # Create a spread array with only 1 true value
    spread_array = [True, False, True, False, False, False, False, False, False, True]
    # Shift the furthest feasible point to the left
    shift_furthest_fesible_point(spread_array, 9, 0)
    assert spread_array == [True, False, True, True, False, False, False, False, False, False]

    spread_array = [False, False, False, True, True, True, False, False, False]
    shift_furthest_fesible_point(spread_array, 5, 8)
    assert spread_array == [False, False, False, True, True, False, False, False, True]


def test_spread_ports():
    raise NotImplementedError()