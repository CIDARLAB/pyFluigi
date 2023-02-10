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

def test_insert_horizontal_spacer_column():
    gnp = generate_new_primitive
    
    cell_list = [
        [gnp(0,0),gnp(1,0),gnp(2,0),gnp(3,0),gnp(4,0)],
        [gnp(0,1),gnp(1,1),gnp(2,1),gnp(3,1),gnp(4,1)],
        [gnp(0,2),gnp(1,2),gnp(2,2),gnp(3,2),gnp(4,2)],
        [gnp(0,3),gnp(1,3),gnp(2,3),gnp(3,3),gnp(4,3)],
        [gnp(0,4),gnp(1,4),gnp(2,4),gnp(3,4),gnp(4,4)],
    ]

    cell_list_test = [
        [gnp(0,0),gnp(1,0),gnp(2,0),gnp(3,0),gnp(4,0)],
        [gnp(0,1),gnp(1,1),gnp(2,1),gnp(3,1),gnp(4,1)],
        [gnp(0,2),gnp(1,2),gnp(2,2),gnp(3,2),gnp(4,2)],
        [gnp(0,3),gnp(1,3),gnp(2,3),gnp(3,3),gnp(4,3)],
        [gnp(0,4),gnp(1,4),gnp(2,4),gnp(3,4),gnp(4,4)],
        [gnp(0,5),gnp(1,5),gnp(2,5),gnp(3,5),gnp(4,5)],
        [gnp(0,6),gnp(1,6),gnp(2,6),gnp(3,6),gnp(4,6)],
    ]

    
    # insert a vertical spacer column at index 2
    spacer_insert = SpacerInsert(
        relative_insert_coordinate=2, # Doesn't matter
        number_of_spacers=2,
        port_topleft_fate= False,
        port_bottomright_fate= False,
        port_topright_fate= False,
        port_bottomleft_fate= False,
    )
    insert_horizontal_spacer_column(cell_list, 2, spacer_insert)

    ccell1 = CompositeCell(cell_list)
    ccell2 = CompositeCell(cell_list_test)
    assert ccell1 == ccell2




