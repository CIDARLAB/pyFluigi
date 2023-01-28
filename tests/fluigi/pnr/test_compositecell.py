from fluigi.pnr.compositecell import ComponentSide, PrimitiveCell
import pytest


def test_primitive_cell_print():
    # Create a primitive cell
    # Print the primitive cell
    # Compare the output to the expected output
    cell = PrimitiveCell(5, 0, 0, [ComponentSide.NORTH, ComponentSide.EAST, ComponentSide.SOUTH, ComponentSide.WEST])

    cell.print_cell()