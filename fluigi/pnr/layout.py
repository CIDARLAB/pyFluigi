import sys
from typing import List, Optional

import networkx as nx
from cairo import SVGSurface
from pymint.mintdevice import MINTDevice

from fluigi.pnr.cell import Cell
from fluigi.pnr.net import Net
from fluigi.pnr.svgdraw import SVGDraw


class Layout:
    def __init__(self) -> None:
        self.cells = dict()
        self.nets = dict()
        self.G = nx.MultiDiGraph()
        self.__original_device = None
        self.__direct_map = []

    def applyLayout(self):
        device = self.__original_device
        for ID in self.__direct_map:
            component = device.getComponent(ID)
            cell = self.cells[ID]
            component.params.set_param("position", [cell.x, cell.y])

    def ensureLegalCoordinates(self):
        # Make sure all the cell coordinates are positive
        minx = sys.maxsize
        miny = sys.maxsize
        maxx = -sys.maxsize
        maxy = -sys.maxsize

        for cell in [self.cells[id] for id in list(self.cells)]:
            if cell.x < minx:
                minx = cell.x
            if cell.x + cell.xdim > maxx:
                maxx = cell.x + cell.xdim

            if cell.y < miny:
                miny = cell.y
            if cell.y + cell.ydim > maxy:
                maxy = cell.y + cell.ydim

    def importMINTwithoutConstraints(self, device: Optional[MINTDevice]) -> None:

        self.__original_device = device

        for component in device.components:
            cell = Cell(component.ID, 0, 0, 1000, 1000)
            self.cells[cell.ID] = cell
            self.G.add_node(cell.ID)
            self.__direct_map.append(cell.ID)

        for connection in device.connections:
            net = Net(connection.ID, connection.source, connection.sinks)
            self.nets[net.ID] = net
            for sink in connection.sinks:
                self.G.add_edge(connection.source.component, sink.component)

    def importMINTwithConstraints(self, device: MINTDevice) -> None:
        # TODO: Process the constraints
        raise Exception("Not Implemented")

    def get_cells(self) -> List[Cell]:
        return [self.cells[id] for id in list(self.cells)]

    def get_nets(self) -> List[Net]:
        return [self.nets[id] for id in list(self.nets)]

    def print_layout(self) -> None:
        draw = SVGDraw()
        for cell in self.cells.keys():
            draw.draw_cell(self.cells[cell])
