from fluigi.pnr.compositecell import PortExists, PrimitiveCell
import pytest


def test_primitive_cell_print():
    # Create a primitive cell
    # Print the primitive cell
    # Compare the output to the expected output
    cell = PrimitiveCell(5, 0, 0, [PortExists.NORTH, PortExists.EAST, PortExists.SOUTH, PortExists.WEST])

    cell.print_cell()