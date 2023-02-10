from fluigi.pnr.sfc.compositecell import CompositeCell
from fluigi.pnr.sfc.primitivecell import ComponentSide, PrimitiveCell

# cell = PrimitiveCell(5, 0, 0, [ComponentSide.NORTH, ComponentSide.EAST, ComponentSide.SOUTH, ComponentSide.WEST])

# cell.print_cell()

# c_cell = CompositeCell([[cell]])

# c_cell.print_cell()

def generate_new_primitive(x, y):
    return PrimitiveCell(x_coord=x, y_coord=y, size=100, ports_exists=[])

gnp = generate_new_primitive
cell_list1 = [
    [gnp(0,0),gnp(1,0),gnp(2,0),gnp(3,0),gnp(4,0)],
    [gnp(0,1),gnp(1,1),gnp(2,1),gnp(3,1),gnp(4,1)],
    [gnp(0,2),gnp(1,2),gnp(2,2),gnp(3,2),gnp(4,2)],
    [gnp(0,3),gnp(1,3),gnp(2,3),gnp(3,3),gnp(4,3)],
    [gnp(0,4),gnp(1,4),gnp(2,4),gnp(3,4),gnp(4,4)],
]

ccell = CompositeCell(cell_list1)
ccell.print_cell_indexes()