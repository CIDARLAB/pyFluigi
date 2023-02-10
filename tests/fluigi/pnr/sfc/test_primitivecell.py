import pytest

from fluigi.pnr.sfc.compositecell import ComponentSide, PrimitiveCell


def test_primitive_cell():
    # Create a primitive cell
    # Print the primitive cell
    # Compare the output to the expected output
    cell = PrimitiveCell(5, 0, 0, [ComponentSide.NORTH, ComponentSide.EAST, ComponentSide.SOUTH, ComponentSide.WEST])

    assert cell.east_port 
    assert cell.west_port
    assert cell.north_port
    assert cell.south_port

def test_activate_port():
    # Create a primitive cell
    # Activate a port
    # Print the primitive cell
    # Compare the output to the expected output
    cell = PrimitiveCell(5, 0, 0, [ComponentSide.EAST, ComponentSide.WEST])
    cell.activate_port(ComponentSide.NORTH)
    cell.activate_port(ComponentSide.SOUTH)
    assert cell.north_port
    assert cell.south_port
    assert cell.east_port
    assert cell.west_port

def test_deactivate_port():
    # Create a primitive cell
    # Deactivate a port
    # Print the primitive cell
    # Compare the output to the expected output
    cell = PrimitiveCell(5, 0, 0, [ComponentSide.NORTH, ComponentSide.SOUTH, ComponentSide.EAST, ComponentSide.WEST])
    cell.deactivate_port(ComponentSide.NORTH)
    cell.deactivate_port(ComponentSide.SOUTH)
    assert not cell.north_port
    assert not cell.south_port
    assert cell.east_port
    assert cell.west_port

def test_equals():
    # Create two primitive cells
    # Compare the two cells
    # Compare the output to the expected output
    cell1 = PrimitiveCell(5, 0, 0, [ComponentSide.NORTH, ComponentSide.EAST, ComponentSide.SOUTH, ComponentSide.WEST])
    cell2 = PrimitiveCell(5, 0, 0, [ComponentSide.NORTH, ComponentSide.EAST, ComponentSide.SOUTH, ComponentSide.WEST])
    assert cell1 == cell2

    # Test for not equal
    cell3 = PrimitiveCell(5, 0, 0, [ComponentSide.NORTH, ComponentSide.EAST, ComponentSide.SOUTH])
    assert not cell1 == cell3