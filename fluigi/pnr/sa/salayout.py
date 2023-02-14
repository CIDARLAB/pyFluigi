from __future__ import annotations

import sys

from fluigi.parameters import AREA_PENALTY, OVERLAP_PENALTY, WIRE_PENALTY
from fluigi.pnr.layout import Layout
from fluigi.pnr.place_and_route import Net as CNet
from fluigi.pnr.place_and_route import PlacementCell as CCell
from fluigi.pnr.place_and_route import Terminal as CTerminal
from fluigi.pnr.sa.layoutgrid import LayoutGrid
from fluigi.pnr.sa.utils import (
    bottom_edge,
    calc_position,
    left_edge,
    manhattan_dist,
    overlap_area,
    right_edge,
    storage,
    top_edge,
)


class SALayout(Layout):
    def __init__(self) -> None:
        super().__init__()
        self.grid: LayoutGrid = LayoutGrid()

        self.cur_top_edge = 0
        self.cur_right_edge = 0
        self.cur_bottom_edge = 0
        self.cur_left_edge = 0

        self.old_cost = 0
        self.old_area = 0
        self.old_overlap = 0
        self.old_wirelength = 0

        self.cur_cost = 0
        self.cur_area = 0
        self.cur_overlap = 0
        self.cur_wirelength = 0

        self.pre_move_comp_overlap = 0
        self.pre_move_wirelength = 0

    def calc_init_cost(self) -> float:
        self.old_area = self.cur_area
        self.cur_area = self.calculate_area()

        self.old_overlap = self.cur_overlap
        self.cur_overlap = self.calculate_overlap()

        self.old_wirelength = self.cur_wirelength
        self.cur_wirelength = self.calculate_wirelength()

        self.old_cost = self.cur_cost
        self.cur_cost = (
            self.cur_wirelength * WIRE_PENALTY + self.cur_area * AREA_PENALTY + self.cur_overlap * OVERLAP_PENALTY
        )
        return self.cur_cost

    def calculate_cost(self, randc: CCell) -> float:
        self.old_wirelength = self.cur_wirelength
        self.cur_wirelength = self.old_wirelength - self.pre_move_wirelength + self.calc_comp_wirelength(randc)

        self.old_area = self.cur_area
        self.cur_area = self.calculate_area()

        self.old_overlap = self.cur_overlap
        self.cur_overlap = self.old_overlap - self.pre_move_comp_overlap + self.calculate_comp_overlap(randc)

        self.old_cost = self.cur_cost
        self.cur_cost = (
            self.cur_wirelength * WIRE_PENALTY + self.cur_area * AREA_PENALTY + self.cur_overlap * OVERLAP_PENALTY
        )
        return self.cur_cost

    def get_delta_cost(self) -> float:
        return self.cur_cost - self.old_cost

    def undo_update_cost(self) -> float:
        self.cur_area = self.old_area
        self.cur_overlap = self.old_overlap
        self.cur_wirelength = self.old_wirelength
        self.cur_cost = self.old_cost
        return self.cur_cost

    def calculate_wirelength(self) -> float:
        wire_sum = 0
        # print("Cell info")
        # for cell in list(self.cells.values()):
        #     print("Cell ID: {}".format(cell.id))
        #     for port in cell.ports:
        #         print("Cell Terminal- {} ({}, {})".format(port.label, port.x, port.y))

        for net in list(self.nets.values()):
            source_cell = net.source
            # print("Source ID: {}".format(source_cell.id))
            source_terminal = net.source_terminal
            # print(
            #     "Source Terminal- {} ({}, {})".format(
            #         source_terminal.label, source_terminal.x, source_terminal.y
            #     )
            # )
            for i in range(len(net.sink_terminals)):
                sink_cell = net.sinks[i]
                # print("Sink ID: {}".format(sink_cell.id))
                sink_terminal = net.sink_terminals[i]
                m_dist = manhattan_dist(source_terminal, sink_terminal)
                penalty = calc_position(source_cell, source_terminal, sink_cell, sink_terminal)
                wire_sum += m_dist + OVERLAP_PENALTY / 2 * penalty
        return wire_sum

    def calc_prev_comp_wirelength(self, c: CCell) -> None:
        # print("prev", self.pre_move_wirelength)
        self.pre_move_wirelength = self.calc_comp_wirelength(c)
        # print("after", self.pre_move_wirelength)
        storage.store_data("instance-premove-comp-wire-length-after-calc", self.pre_move_wirelength)

    def calc_comp_wirelength(self, c: CCell) -> float:
        wire_sum = 0
        # TODO : include the graph into the data structure
        for net in list(self.nets.values()):
            source_cell = net.source
            source_terminal = net.source_terminal
            for i in range(len(net.sink_terminals)):
                sink_cell = net.sinks[i]
                sink_terminal = net.sink_terminals[i]
                dist = manhattan_dist(source_terminal, sink_terminal)
                penalty = calc_position(source_cell, source_terminal, sink_cell, sink_terminal)
                wire_sum += dist + OVERLAP_PENALTY / 2 * penalty
        storage.store_data("instance-comp-wirelenght-randc", wire_sum)

        # print("ret wiresum ", wire_sum)
        return wire_sum

    def calc_prev_comp_overlap(self, randc: CCell) -> None:
        self.pre_move_comp_overlap = self.calculate_comp_overlap(randc)

    def calculate_area(self) -> float:
        """[summary]

        Returns:
            int: [description]
        """

        min_left = min_top = sys.maxsize
        max_right = max_bottom = 0

        for cell in list(self.cells.values()):
            if left_edge(cell) < min_left:
                min_left = left_edge(cell)
            if right_edge(cell) > max_right:
                max_right = right_edge(cell)
            if top_edge(cell) < min_top:
                min_top = top_edge(cell)
            if bottom_edge(cell) > max_bottom:
                max_bottom = bottom_edge(cell)

        self.cur_bottom_edge = max_bottom
        self.cur_top_edge = min_top
        self.cur_left_edge = min_left
        self.cur_right_edge = max_right

        return (max_bottom - min_top) * (max_right - min_left)

    # TODO - RENAME THIS LATER ON
    def calculate_overlap(self) -> float:
        overlap_sum = 0
        cells = list(self.cells.values())
        for i in range(len(cells)):
            c1 = cells[i]
            for j in range(i + 1, len(cells)):
                c2 = cells[j]
                overlap_sum += overlap_area(c1, c2)

        return overlap_sum

    def calculate_comp_overlap(self, randc) -> float:
        return self.grid.calculate_component_overlap(randc)

    def reset(self):
        self.old_cost = 0
        self.old_area = 0
        self.old_overlap = 0
        self.old_wirelength = 0

        self.cur_cost = 0
        self.cur_area = 0
        self.cur_overlap = 0
        self.cur_wirelength = 0

        self.cur_right_edge = 0
        self.cur_left_edge = 0
        self.cur_bottom_edge = 0
        self.cur_top_edge = 0

    def calculate_init_cost(self):
        self.old_cost = self.cur_cost
        self.old_overlap = self.cur_overlap
        self.old_wirelength = self.cur_wirelength
        self.cur_area = self.calculate_area()
        self.cur_overlap = self.calculate_overlap()
        self.cur_wirelength = self.calculate_wirelength()
        self.cur_cost = (
            self.cur_wirelength * WIRE_PENALTY + self.cur_area * AREA_PENALTY + self.cur_overlap * OVERLAP_PENALTY
        )

        return self.cur_cost
