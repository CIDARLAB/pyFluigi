import random
from enum import Enum
from math import floor
from typing import Dict, List, Optional

from fluigi.pnr.place_and_route import PlacementCell as CCell
from fluigi.pnr.place_and_route import Terminal as CTerminal


class TerminalLocation(Enum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3


def left_edge(cell: CCell) -> int:
    return cell.x - cell.component_spacing


def right_edge(cell: CCell) -> int:
    return cell.x + cell.x_span + cell.component_spacing


def top_edge(cell: CCell) -> int:
    return cell.y - cell.component_spacing


def bottom_edge(cell: CCell) -> int:
    return cell.y + cell.component_spacing


def overlaps(c1: CCell, c2: CCell) -> bool:
    if left_edge(c1) > right_edge(c2):
        return False
    elif right_edge(c1) < left_edge(c2):
        return False
    elif bottom_edge(c1) < top_edge(c2):
        return False
    elif top_edge(c1) > bottom_edge(c2):
        return False
    else:
        return True


def overlap_x(c1: CCell, c2: CCell) -> int:
    left = max(left_edge(c1), left_edge(c2))
    right = max(right_edge(c1), right_edge(c2))
    return right - left


def overlap_y(c1: CCell, c2: CCell) -> int:
    top = max(top_edge(c1), top_edge(c2))
    bottom = max(bottom_edge(c1), bottom_edge(c2))
    return bottom - top


def overlap_area(c1: CCell, c2: CCell) -> int:
    left = max(left_edge(c1), left_edge(c2))
    right = min(right_edge(c1), right_edge(c2))
    top = max(top_edge(c1), top_edge(c2))
    bottom = min(bottom_edge(c1), bottom_edge(c2))

    return (bottom - top) * (right - left)


def manhattan_dist(source: CTerminal, sink: CTerminal) -> int:
    return abs(source.x - sink.x) + abs(source.y - sink.y)


def calc_position(
    source_cell: CCell,
    source_terminal: CTerminal,
    sink_cell: CCell,
    sink_terminal: CTerminal,
) -> int:
    sx = source_terminal.x
    sy = source_terminal.y

    tx = sink_cell.x
    ty = sink_cell.y

    s_ind = get_terminal_location(source_terminal, source_cell)
    t_ind = get_terminal_location(sink_terminal, sink_cell)

    s_penalty = 0
    t_penalty = 0

    if s_ind is TerminalLocation.TOP:
        if sy < ty:
            s_penalty = 1
    elif s_ind is TerminalLocation.RIGHT:
        if sx > tx:
            s_penalty = 1
    elif s_ind is TerminalLocation.BOTTOM:
        if sy > ty:
            s_penalty = 1
    else:
        if sx < tx:
            s_penalty = 1

    if t_ind is TerminalLocation.TOP:
        if ty < sy:
            t_penalty = 1
    elif t_ind is TerminalLocation.RIGHT:
        if tx > sx:
            t_penalty = 1
    elif t_ind is TerminalLocation.BOTTOM:
        if ty > sy:
            t_penalty = 1
    else:
        if tx < sx:
            t_penalty = 1

    return s_penalty + t_penalty


def get_terminal(cell, label) -> CTerminal:
    # warning ! only access using for i in range pattern
    for i, item in enumerate(cell.ports):
        if item.label == label:
            return item
    raise Exception("Could not find terminal in cell")


def get_terminal_location(terminal: CTerminal, cell: CCell) -> TerminalLocation:
    # TODO - Incorporate Rotation at some point to
    # allow us to rotate the matrix
    top_dist = abs(terminal.rel_y)
    right_dist = abs(terminal.rel_x - cell.x_span)
    bottom_dist = abs(terminal.rel_y - cell.y_span)
    left_dist = abs(terminal.rel_x)

    dist_array = [top_dist, right_dist, bottom_dist, left_dist]

    index = dist_array.index(min(dist_array))

    if index == 0:
        return TerminalLocation.TOP
    elif index == 1:
        return TerminalLocation.RIGHT
    elif index == 2:
        return TerminalLocation.BOTTOM
    else:
        return TerminalLocation.RIGHT


def update_terminals(cell: CCell):

    for i, item in enumerate(cell.ports):
        item.compute_absolute_positions(cell.x, cell.y)

    # print("After Update", [(t.x, t.y) for t in cell.ports])


def select_random_component(list_components):
    return list_components[floor(random.random() * len(list_components))]


# TODO - Move to C++ api candidate
def move(c: CCell, delta_x: int, delta_y: int):
    c.x += delta_x
    c.y += delta_y
    update_terminals(c)


class AlgDataStorage:
    def __init__(self) -> None:
        super().__init__()
        self._data: Dict[str, List[Optional[float]]] = {}
        self._size = 0

    def store_data(self, param, data):
        if param in self._data:
            current_len = len(self._data[param])
            for i in range(current_len, self._size - 1):
                self._data[param].append(None)
            self._data[param].append(data)
        else:
            self._data[param] = []
            # fill None's as padding
            for i in range(self._size - 1):
                self._data[param].append(None)
            self._data[param].append(data)

        self._size = len(self._data[param])

    def print_data(self):
        self.pad_data()
        print(",".join(self._data.keys()))
        for i in range(self._size):
            print(",".join([str(self._data[key][i]) for key in self._data]))

    def save_data(self):
        self.pad_data()
        text = ",".join(self._data.keys()) + "\n"
        for i in range(self._size):
            text += (",".join([str(self._data[key][i]) for key in self._data])) + "\n"
        f = open("SA-Data.csv", "w")
        f.write(text)
        f.close()

    def new_stage(self):
        self._size += 1
        self.pad_data()

    def pad_data(self):
        for key in self._data:
            for i in range(len(self._data[key]), self._size):
                self._data[key].append(None)


storage = AlgDataStorage()
