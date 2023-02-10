from fluigi.pnr.sfc.compositecell import CompositeCell
from fluigi.pnr.sfc.primitivecell import PrimitiveCell
from fluigi.pnr.sfc.spacer_insert import SpacerInsert, get_spacer_size, insert_horizontal_spacer_column, insert_vertical_spacer_column
from parchmint.port import Port
from tests.conftest import generate_new_primitive, cell_test1, cell_test2, cell_test3


def test_get_spacer_size():
    # Note - SPACER_THRESHOLD is 5000 
    # this needs to be set in parameters.py
    assert get_spacer_size(200, 1000) == 0
    assert get_spacer_size(1000, 7000) == 1

def test_generate_spacers():
    raise NotImplementedError()

def test_insert_vertical_spacer_column():
    raise NotImplementedError()

def test_insert_horizontal_spacer_column(cell_test1, cell_test2, cell_test3):
    

    ccell1 = CompositeCell(cell_test1)

    ccell_ref = CompositeCell(cell_test3)
    
    # insert a vertical spacer column at index 2
    spacer_insert = SpacerInsert(
        relative_insert_coordinate=2, # Doesn't matter
        number_of_spacers=2,
        port_topleft_fate= False,
        port_bottomright_fate= False,
        port_topright_fate= False,
        port_bottomleft_fate= False,
    )
    insert_horizontal_spacer_column(ccell1.cells, 2, spacer_insert)

    assert ccell1 == ccell_ref




