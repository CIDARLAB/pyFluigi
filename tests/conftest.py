import pytest
from parchmint.component import Component
from parchmint.port import Port

from fluigi.pnr.sfc.primitivecell import ComponentSide, PrimitiveCell


@pytest.fixture
def component():
    # Create a component
    component = Component(
        name="test_component",
        ID="test_component",
        xpos=0,
        ypos=0,
        xspan=1000,
        yspan=1000,
    )
    return component


@pytest.fixture
def cell_test1():
    gnp = generate_new_primitive
    cell_list1 = [
        [gnp(0, 0), gnp(1, 0), gnp(2, 0), gnp(3, 0), gnp(4, 0)],
        [gnp(0, 1), gnp(1, 1), gnp(2, 1), gnp(3, 1), gnp(4, 1)],
        [gnp(0, 2), gnp(1, 2), gnp(2, 2), gnp(3, 2), gnp(4, 2)],
        [gnp(0, 3), gnp(1, 3), gnp(2, 3), gnp(3, 3), gnp(4, 3)],
        [gnp(0, 4), gnp(1, 4), gnp(2, 4), gnp(3, 4), gnp(4, 4)],
    ]
    return cell_list1


@pytest.fixture
def cell_test2():
    gnp = generate_new_primitive
    cell_list2 = [
        [gnp(0, 0), gnp(1, 0), gnp(2, 0), gnp(3, 0), gnp(4, 0)],
        [gnp(0, 1), gnp(1, 1), gnp(2, 1), gnp(3, 1), gnp(4, 1)],
        [gnp(0, 2), gnp(1, 2), gnp(2, 2), gnp(3, 2), gnp(4, 2)],
        [gnp(0, 3), gnp(1, 3), gnp(2, 3), gnp(3, 3), gnp(4, 3)],
        [gnp(0, 4), gnp(1, 4), gnp(2, 4), gnp(3, 4), gnp(4, 4)],
    ]
    return cell_list2


@pytest.fixture
def cell_test3():
    gnp = generate_new_primitive
    cell_list3 = [
        [gnp(0, 0), gnp(1, 0), gnp(2, 0), gnp(3, 0), gnp(4, 0)],
        [gnp(0, 1), gnp(1, 1), gnp(2, 1), gnp(3, 1), gnp(4, 1)],
        [gnp(0, 2), gnp(1, 2), gnp(2, 2), gnp(3, 2), gnp(4, 2)],
        [gnp(0, 3), gnp(1, 3), gnp(2, 3), gnp(3, 3), gnp(4, 3)],
        [gnp(0, 4), gnp(1, 4), gnp(2, 4), gnp(3, 4), gnp(4, 4)],
        [gnp(0, 5), gnp(1, 5), gnp(2, 5), gnp(3, 5), gnp(4, 5)],
        [gnp(0, 6), gnp(1, 6), gnp(2, 6), gnp(3, 6), gnp(4, 6)],
    ]
    return cell_list3


@pytest.fixture
def cell_test4():
    gnp = generate_new_primitive
    cell_list3 = [
        [gnp(0, 0), gnp(1, 0), gnp(2, 0), gnp(3, 0), gnp(4, 0)],
        [gnp(0, 1), gnp(1, 1), gnp(2, 1), gnp(3, 1), gnp(4, 1)],
        [gnp(0, 2), gnp(1, 2), gnp(2, 2), gnp(3, 2), gnp(4, 2)],
        [gnp(0, 3), gnp(1, 3), gnp(2, 3), gnp(3, 3), gnp(4, 3)],
        [gnp(0, 4), gnp(1, 4), gnp(2, 4), gnp(3, 4), gnp(4, 4)],
        [gnp(0, 5), gnp(1, 5), gnp(2, 5), gnp(3, 5), gnp(4, 5)],
        [gnp(0, 6), gnp(1, 6), gnp(2, 6), gnp(3, 6), gnp(4, 6)],
        [gnp(0, 7), gnp(1, 7), gnp(2, 7), gnp(3, 7), gnp(4, 7)],
        [gnp(0, 8), gnp(1, 8), gnp(2, 8), gnp(3, 8), gnp(4, 8)],
    ]

    # Set the ports for the new insertion (WEST, EAST of row 2, 5)
    cell_list3[2][0].activate_port(ComponentSide.WEST)
    cell_list3[2][-1].activate_port(ComponentSide.EAST)
    cell_list3[5][0].activate_port(ComponentSide.WEST)
    cell_list3[5][-1].activate_port(ComponentSide.EAST)
    return cell_list3


@pytest.fixture
def cell_test5():
    gnp = generate_new_primitive
    cell_list1 = [
        [gnp(0, 0), gnp(1, 0), gnp(2, 0), gnp(3, 0), gnp(4, 0), gnp(5, 0), gnp(6, 0)],
        [gnp(0, 1), gnp(1, 1), gnp(2, 1), gnp(3, 1), gnp(4, 1), gnp(5, 1), gnp(6, 1)],
        [gnp(0, 2), gnp(1, 2), gnp(2, 2), gnp(3, 2), gnp(4, 2), gnp(5, 2), gnp(6, 2)],
        [gnp(0, 3), gnp(1, 3), gnp(2, 3), gnp(3, 3), gnp(4, 3), gnp(5, 3), gnp(6, 3)],
        [gnp(0, 4), gnp(1, 4), gnp(2, 4), gnp(3, 4), gnp(4, 4), gnp(5, 4), gnp(6, 4)],
    ]

    return cell_list1


@pytest.fixture
def cell_test6():
    gnp = generate_new_primitive
    cell_list1 = [
        [gnp(0, 0), gnp(1, 0), gnp(2, 0), gnp(3, 0), gnp(4, 0), gnp(5, 0), gnp(6, 0), gnp(7, 0), gnp(8, 0)],
        [gnp(0, 1), gnp(1, 1), gnp(2, 1), gnp(3, 1), gnp(4, 1), gnp(5, 1), gnp(6, 1), gnp(7, 1), gnp(8, 1)],
        [gnp(0, 2), gnp(1, 2), gnp(2, 2), gnp(3, 2), gnp(4, 2), gnp(5, 2), gnp(6, 2), gnp(7, 2), gnp(8, 2)],
        [gnp(0, 3), gnp(1, 3), gnp(2, 3), gnp(3, 3), gnp(4, 3), gnp(5, 3), gnp(6, 3), gnp(7, 3), gnp(8, 3)],
        [gnp(0, 4), gnp(1, 4), gnp(2, 4), gnp(3, 4), gnp(4, 4), gnp(5, 4), gnp(6, 4), gnp(7, 4), gnp(8, 4)],
    ]

    # Set the ports for the new insertion (NORTH, SOUTH of row 2, 5)
    cell_list1[0][2].activate_port(ComponentSide.NORTH)
    cell_list1[-1][2].activate_port(ComponentSide.SOUTH)
    cell_list1[0][5].activate_port(ComponentSide.NORTH)
    cell_list1[-1][5].activate_port(ComponentSide.SOUTH)

    return cell_list1


def generate_new_primitive(x, y):
    return PrimitiveCell(x_coord=x, y_coord=y, size=100, ports_exists=[])


@pytest.fixture
def comp1() -> Component:
    comp1 = Component(
        ID="comp1",
        name="comp1",
        xpos=0,
        ypos=0,
        xspan=1000,
        yspan=10000,
        ports_list=[
            Port(
                label="1",
                layer="flow",
                x=500,
                y=0,
            ),
            Port(
                label="2",
                layer="flow",
                x=1000,
                y=500,
            ),
            Port(
                label="3",
                layer="flow",
                x=1000,
                y=5000,
            ),
            Port(
                label="4",
                layer="flow",
                x=1000,
                y=9500,
            ),
            Port(
                label="5",
                layer="flow",
                x=500,
                y=10000,
            ),
            Port(
                label="6",
                layer="flow",
                x=0,
                y=5000,
            ),
            Port(
                label="7",
                layer="flow",
                x=0,
                y=500,
            ),
        ],
    )
    return comp1
