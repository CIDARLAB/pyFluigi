from fluigi.pnr.sfc.compositecell import CompositeCell
from fluigi.pnr.sfc.primitivecell import ComponentSide, PrimitiveCell

cell = PrimitiveCell(5, 0, 0, [ComponentSide.NORTH, ComponentSide.EAST, ComponentSide.SOUTH, ComponentSide.WEST])

cell.print_cell()

c_cell = CompositeCell([[cell]])

c_cell.print_cell()