from fluigi.parameters import SPACER_THRESHOLD
from fluigi.pnr.sfc.compositecell import CompositeCell
from fluigi.pnr.sfc.primitivecell import ComponentSide, PrimitiveCell
from parchmint.component import Component
from parchmint.port import Port
from tests.conftest import generate_new_primitive, cell_test1, cell_test2, cell_test3
import pytest


@pytest.fixture
def ccell_port_ref():
    return CompositeCell(
        [[
            PrimitiveCell(
                x_coord=0,
                y_coord=0,
                size=SPACER_THRESHOLD,
                ports_exists=[
                    ComponentSide.NORTH,
                    ComponentSide.SOUTH,
                    ComponentSide.EAST,
                    ComponentSide.WEST,
                ]
            )
        ]]
    )


def test_from_parchmint_component(ccell_port_ref):
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
                x = 500,
                y = 500,
            )
        ]
    )

    ccell_port = CompositeCell.from_parchmint_component(port_component)

    assert ccell_port == ccell_port_ref



def test_equals(cell_test1, cell_test2, cell_test3):

    assert CompositeCell(cell_test1) == CompositeCell(cell_test2)

    assert not CompositeCell(cell_test1) == CompositeCell(cell_test3)

    # TODO - Generate more test cases


