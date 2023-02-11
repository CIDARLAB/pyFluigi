import pytest
from parchmint.component import Component
from parchmint.port import Port
from tests.conftest import cell_test1, cell_test2, cell_test3, generate_new_primitive

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
def ccell_comp2_ref():
    gpd = generate_new_primitive
    ccell = CompositeCell(
        [
            [gpd(0, 0), gpd(1, 0), gpd(2, 0), gpd(3, 0), gpd(4, 0)],
            [gpd(0, 1), gpd(1, 1), gpd(2, 1), gpd(3, 1), gpd(4, 1)],
            [gpd(0, 2), gpd(1, 2), gpd(2, 2), gpd(3, 2), gpd(4, 2)],
        ]
    )
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


def test_initialize_port(cell_list1):
    CompositeCell.__initialize_ports(cell_list1, ComponentSide.NORTH, [])


def test_from_parchmint_component(ccell_port_ref, ccell_comp1_ref, comp1: Component):
    # Create a simple square parchmint component with a single port in the center

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

    ccell_comp1 = CompositeCell.from_parchmint_component(comp1, False, False)
    assert ccell_comp1 == ccell_comp1_ref


def test_equals(cell_test1, cell_test2, cell_test3):

    assert CompositeCell(cell_test1) == CompositeCell(cell_test2)

    assert not CompositeCell(cell_test1) == CompositeCell(cell_test3)

    # TODO - Generate more test cases
