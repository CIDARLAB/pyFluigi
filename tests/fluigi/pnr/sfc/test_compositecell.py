from typing import List

import pytest
from parchmint.component import Component
from parchmint.port import Port
from tests.conftest import (
    cell_test1,
    cell_test2,
    cell_test3,
    cell_test_even_x,
    generate_new_primitive,
)

from fluigi.parameters import SPACER_THRESHOLD
from fluigi.pnr.sfc.compositecell import CompositeCell
from fluigi.pnr.sfc.primitivecell import ComponentSide, PrimitiveCell


@pytest.fixture
def ccell_port_ref():
    return CompositeCell(
        [
            [
                PrimitiveCell(
                    x_coord=0,
                    y_coord=0,
                    size=SPACER_THRESHOLD,
                    ports_exists=[
                        ComponentSide.NORTH,
                        ComponentSide.SOUTH,
                        ComponentSide.EAST,
                        ComponentSide.WEST,
                    ],
                )
            ]
        ]
    )


@pytest.fixture
def ccell_comp1_ref_base():
    gpd = generate_new_primitive
    ccell = CompositeCell(
        [
            [gpd(0, 0)],
            [gpd(0, 1)],
            [gpd(0, 2)],
        ]
    )

    # Set the port (0,0)
    ccell.activate_port(0, 0, ComponentSide.NORTH)
    ccell.activate_port(0, 0, ComponentSide.WEST)
    ccell.activate_port(0, 0, ComponentSide.EAST)

    # Set the port (0,1)
    ccell.activate_port(0, 1, ComponentSide.EAST)

    # Set the port (0,2)
    ccell.activate_port(0, 2, ComponentSide.SOUTH)
    ccell.activate_port(0, 2, ComponentSide.WEST)
    ccell.activate_port(0, 2, ComponentSide.EAST)

    return ccell


@pytest.fixture
def ccell_comp1_ref_base_90():
    gpd = generate_new_primitive
    ccell = CompositeCell(
        [
            [gpd(0, 0), gpd(1, 0), gpd(2, 0)],
        ]
    )

    # Set the port (0,2)
    ccell.activate_port(2, 0, ComponentSide.NORTH)
    ccell.activate_port(2, 0, ComponentSide.EAST)
    ccell.activate_port(2, 0, ComponentSide.SOUTH)

    # Set the port (0,1)
    ccell.activate_port(1, 0, ComponentSide.SOUTH)

    # Set the port (0,2)
    ccell.activate_port(0, 0, ComponentSide.NORTH)
    ccell.activate_port(0, 0, ComponentSide.WEST)
    ccell.activate_port(0, 0, ComponentSide.SOUTH)

    return ccell


@pytest.fixture
def ccell_comp1_ref():
    gpd = generate_new_primitive
    ccell = CompositeCell(
        [
            [gpd(0, 0)],
            [gpd(0, 1)],
            [gpd(0, 2)],
        ]
    )

    # Set the port (0,0)
    ccell.activate_port(0, 0, ComponentSide.NORTH)
    ccell.activate_port(0, 0, ComponentSide.WEST)
    ccell.activate_port(0, 0, ComponentSide.EAST)

    # Set the port (0,1)
    ccell.activate_port(0, 1, ComponentSide.EAST)
    ccell.activate_port(0, 1, ComponentSide.WEST)

    # Set the port (0,2)
    ccell.activate_port(0, 2, ComponentSide.SOUTH)
    ccell.activate_port(0, 2, ComponentSide.WEST)
    ccell.activate_port(0, 2, ComponentSide.EAST)

    return ccell


@pytest.fixture
def ccell_comp2_ref_base():
    gpd = generate_new_primitive
    ccell = CompositeCell(
        [
            [gpd(0, 0), gpd(1, 0), gpd(2, 0), gpd(3, 0), gpd(4, 0)],
            [gpd(0, 1), gpd(1, 1), gpd(2, 1), gpd(3, 1), gpd(4, 1)],
            [gpd(0, 2), gpd(1, 2), gpd(2, 2), gpd(3, 2), gpd(4, 2)],
        ]
    )
    # Set the north ports in the first row
    ccell.activate_port(0, 0, ComponentSide.NORTH)
    ccell.activate_port(1, 0, ComponentSide.NORTH)
    ccell.activate_port(2, 0, ComponentSide.NORTH)
    ccell.activate_port(3, 0, ComponentSide.NORTH)
    ccell.activate_port(4, 0, ComponentSide.NORTH)

    # Set the south ports in the last row
    ccell.activate_port(0, 2, ComponentSide.SOUTH)
    ccell.activate_port(1, 2, ComponentSide.SOUTH)
    ccell.activate_port(2, 2, ComponentSide.SOUTH)
    ccell.activate_port(3, 2, ComponentSide.SOUTH)
    ccell.activate_port(4, 2, ComponentSide.SOUTH)

    # Set the east ports in the last column
    ccell.activate_port(4, 0, ComponentSide.EAST)
    ccell.activate_port(4, 1, ComponentSide.EAST)
    ccell.activate_port(4, 2, ComponentSide.EAST)

    # Set the west ports in the first column
    ccell.activate_port(0, 0, ComponentSide.WEST)
    ccell.activate_port(0, 1, ComponentSide.WEST)
    ccell.activate_port(0, 2, ComponentSide.WEST)

    return ccell


@pytest.fixture
def ccell_comp3_ref():
    gpd = generate_new_primitive
    ccell = CompositeCell(
        [
            [gpd(0, 0), gpd(1, 0), gpd(2, 0)],
            [gpd(0, 1), gpd(1, 1), gpd(2, 1)],
        ]
    )
    return ccell


@pytest.fixture
def ccell_comp4_ref():
    gpd = generate_new_primitive
    ccell = CompositeCell(
        [
            [gpd(0, 0), gpd(1, 0), gpd(2, 0), gpd(3, 0)],
        ]
    )
    return ccell


def test_initialize_ports(cell_test1, cell_test_even_x: List[List[PrimitiveCell]]):
    # CASES: 1. Port is in the center of the cell
    #        2. Odd number of ports and even number of cells
    #        3. Even number of ports and even number of cells
    #        4. Even number of ports and odd number of cells
    #        5. Odd number of ports and odd number of cells

    # CASE 1. Being checked in the test_from_parchmint_component

    # CASE 2. Odd number of ports and even number of cells
    # Check that the it raises an error
    with pytest.raises(ValueError):
        CompositeCell.initialize_ports(
            cell_test_even_x,
            ComponentSide.NORTH,
            [
                Port(label="1", layer="flow", x=1000, y=0),
                Port(label="2", layer="flow", x=1000, y=100),
                Port(label="3", layer="flow", x=1000, y=500),
            ],
        )

    # Check for a all the different cases of ports and size
    # CASE 3. Even number of ports and even number of cells
    CompositeCell.initialize_ports(
        cell_test_even_x,
        ComponentSide.SOUTH,
        [
            Port(label="1", layer="flow", x=0, y=1000),
            Port(label="2", layer="flow", x=100, y=1000),
            Port(label="3", layer="flow", x=500, y=1000),
            Port(label="3", layer="flow", x=700, y=1000),
        ],
    )

    # Check that the ports are initialized correctly
    assert [cell.south_port for cell in cell_test_even_x[-1]] == [False, False, True, True, True, True, False, False]

    # CASE 4. Even number of ports and odd number of cells
    CompositeCell.initialize_ports(
        cell_test1,
        ComponentSide.NORTH,
        [
            Port(label="1", layer="flow", x=0, y=0),
            Port(label="2", layer="flow", x=100, y=0),
            Port(label="3", layer="flow", x=500, y=0),
            Port(label="4", layer="flow", x=1000, y=0),
        ],
    )

    # Check that the ports are initialized correctly
    assert [cell.north_port for cell in cell_test1[0]] == [True, True, False, True, True]

    # CASE 5. Odd number of ports and odd number of cells
    CompositeCell.initialize_ports(
        cell_test1,
        ComponentSide.WEST,
        [
            Port(label="1", layer="flow", x=0, y=0),
            Port(label="2", layer="flow", x=0, y=100),
            Port(label="3", layer="flow", x=0, y=500),
        ],
    )

    # Check that the ports are initialized correctly
    assert [row[0].west_port for row in cell_test1] == [False, True, True, True, False]


def test_from_parchmint_component(
    ccell_port_ref, ccell_comp1_ref_base, ccell_comp2_ref_base, comp1: Component, comp2: Component
):
    # Create a simple square parchmint component with a single port in the center

    # Case 1
    # ----X----
    # |       |
    # X       X
    # |       |
    # ----X----

    port_component = Component(
        ID="port",
        name="port",
        xpos=0,
        ypos=0,
        xspan=1000,
        yspan=1000,
        ports_list=[
            Port(
                label="1",
                layer="flow",
                x=500,
                y=500,
            )
        ],
    )

    ccell_port = CompositeCell.from_parchmint_component(port_component)

    assert ccell_port == ccell_port_ref

    # Case 2
    # ----X----
    # |       |
    # X       X
    # |       |
    # ---------
    # ---------
    # |       |
    # |       X
    # |       |
    # ---------
    # ---------
    # |       |
    # X       X
    # |       |
    # ----X----

    ccell_comp1 = CompositeCell.from_parchmint_component(comp1, False, False)
    assert ccell_comp1 == ccell_comp1_ref_base

    # Case 3

    ccell_comp2 = CompositeCell.from_parchmint_component(comp2, False, False)

    assert ccell_comp2 == ccell_comp2_ref_base


def test_equals(cell_test1, cell_test2, cell_test3):
    assert CompositeCell(cell_test1) == CompositeCell(cell_test2)

    assert not CompositeCell(cell_test1) == CompositeCell(cell_test3)

    # TODO - Generate more test cases


def test_rotate_clockwise(ccell_comp1_ref_base, ccell_comp1_ref_base_90):
    ccell_comp1_ref_base.rotate_clockwise()

    assert ccell_comp1_ref_base == ccell_comp1_ref_base_90
