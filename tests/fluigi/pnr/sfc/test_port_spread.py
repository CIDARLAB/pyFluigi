import pytest
from fluigi.pnr.sfc.port_spread import generate_bin_map
from fluigi.pnr.sfc.primitivecell import ComponentSide

from parchmint.port import Port

@pytest.fixture
def north_ports():
    # Create 4 ports in the north side
    port_north_1 = Port("north_1",x=250, y=0)
    port_north_2 = Port("north_2",x=500, y=0)
    port_north_3 = Port("north_3",x=750, y=0)
    port_north_4 = Port("north_4",x=1000, y=0)

    return [port_north_1, port_north_2, port_north_3, port_north_4]


def test_try_shift_left():
    raise NotImplementedError()

def test_try_shift_right():
    raise NotImplementedError()

def test_generate_bin_map(north_ports, component):
    # Test the bin map generation for the north ports
    # For different kinds of spread arrays
    # This is a 10 spread array
    spread_array = [True, True, True, True, True, True, True, True, True, True]
    bin_map = generate_bin_map(spread_array, north_ports, component, ComponentSide.NORTH)
    assert bin_map == {0: 2, 1: 5, 2: 7, 3: 10}


def test_furthest_feasible_point():
    raise NotImplementedError()

