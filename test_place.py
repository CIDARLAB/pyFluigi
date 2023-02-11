from fluigi.pnr.place_and_route import *

terminals1 = []
terminals2 = []

t1 = Terminal("Terminal 1", 0, 5)
t2 = Terminal("Terminal 2", 10, 5)

terminals1.append(t1)
terminals2.append(t2)

cell1 = PlacementCell("0", 0, 0, 10, 10, 10, terminals1)

cell2 = PlacementCell("1", 25, 25, 10, 10, 10, terminals2)

sink_cells = []
sink_cells.append(cell2)

net1 = Net("n0", cell1, t1, sink_cells, terminals2)

cells = []
cells.append(cell1)
cells.append(cell2)
nets = []
nets.append(net1)

constraints = []

placer = Placer(cells, nets, constraints)

placer.place(50, 50)
