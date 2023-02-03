from fluigi.pnr.sfc.compositecell import ComponentSide, PrimitiveCell
import pytest


def test_primitive_cell_print():
    # Create a primitive cell
    # Print the primitive cell
    # Compare the output to the expected output
    cell = PrimitiveCell(5, 0, 0, [ComponentSide.NORTH, ComponentSide.EAST, ComponentSide.SOUTH, ComponentSide.WEST])

    assert cell.east_port 
    assert cell.west_port
    assert cell.north_port
    assert cell.south_port