from __future__ import annotations
from typing import Dict, List, Tuple

from fluigi.parameters import DEVICE_X_DIM, DEVICE_Y_DIM, LAMBDA, SA_GRID_BLOCK_SIZE
from fluigi.pnr.place_and_route import PlacementCell as CCell
from fluigi.pnr.sa.utils import (
    bottom_edge,
    left_edge,
    move,
    overlap_area,
    right_edge,
    top_edge,
)


class LayoutGrid:
    def __init__(self) -> None:
        super().__init__()
        self.x_offset_memory = 0
        self.y_offset_memory = 0
        self.layout_grid: Dict[Tuple[int, int], List[CCell]] = {}
        self.c = None

    def new_move(self, moved_cell: CCell, x: int, y: int) -> None:
        c = moved_cell
        x_offset = x
        y_offset = y

        cx = c.x
        cy = c.y

        if cx + x_offset + c.x_span > DEVICE_X_DIM / LAMBDA:
            x_offset = 0
        elif cx + x_offset < 0:
            x_offset = 0

        if cy + c.y_span + y_offset > DEVICE_Y_DIM / LAMBDA:
            y_offset = 0
        elif cy + y_offset < 0:
            y_offset = 0

        # print("Temporary Moving Cell by: ({}, {})".format(x_offset, y_offset))
        move(c, x_offset, y_offset)
        # print("Temporary Moved Cell {} : ({}, {})".format(c.id, c.x, c.y))
        self.c = c
        self.x_offset_memory = x_offset
        self.y_offset_memory = y_offset

    def apply_move(self) -> None:
        if self.c is None:
            raise Exception("Could not apply move becuase current component is set to None")
        move(self.c, -self.x_offset_memory, -self.y_offset_memory)

        self.remove_component(self.c)

        move(self.c, self.x_offset_memory, self.y_offset_memory)
        # print(
        #     "Saving Move, new location of cell {}: ({}, {})".format(
        #         self.c.id, self.c.x, self.c.y
        #     )
        # )
        self.add_component(self.c)

    def undo_move(self) -> None:
        if self.c is None:
            raise Exception("Could not apply move becuase current component is set to None")

        move(self.c, -self.x_offset_memory, -self.y_offset_memory)

    def remove_component(self, c: CCell) -> None:
        layout_grid = self.layout_grid
        minX = int(left_edge(c) / SA_GRID_BLOCK_SIZE)
        maxX = int(right_edge(c) / SA_GRID_BLOCK_SIZE)
        minY = int(top_edge(c) / SA_GRID_BLOCK_SIZE)
        maxY = int(bottom_edge(c) / SA_GRID_BLOCK_SIZE)
        for i in range(minX, maxX):
            for j in range(minY, maxY):
                key = (i, j)
                cell_list = layout_grid[key]
                cell_list.remove(c)
                if len(cell_list) == 0:
                    del layout_grid[key]

    def add_component(self, c: CCell) -> None:
        layout_grid = self.layout_grid
        minX = int(left_edge(c) / SA_GRID_BLOCK_SIZE)
        maxX = int(right_edge(c) / SA_GRID_BLOCK_SIZE)
        minY = int(top_edge(c) / SA_GRID_BLOCK_SIZE)
        maxY = int(bottom_edge(c) / SA_GRID_BLOCK_SIZE)
        for i in range(minX, maxX):
            for j in range(minY, maxY):
                key = (i, j)
                # Initialize the array if key not present
                if key not in layout_grid:
                    layout_grid[key] = []

                cell_list = layout_grid[key]
                cell_list.append(c)

    def calcualte_overlap(self) -> int:
        overlap_sum = 0
        for cell_list in list(self.layout_grid.values()):
            for i, c1 in enumerate(cell_list):
                for j in range(i + 1, len(cell_list)):
                    c2 = cell_list[j]
                    overlap_sum += overlap_area(c1, c2)
        return overlap_sum

    def calculate_component_overlap(self, randc) -> int:
        overlap_sum = 0
        minX = int(left_edge(randc) / SA_GRID_BLOCK_SIZE)
        maxX = int(right_edge(randc) / SA_GRID_BLOCK_SIZE)
        minY = int(top_edge(randc) / SA_GRID_BLOCK_SIZE)
        maxY = int(bottom_edge(randc) / SA_GRID_BLOCK_SIZE)
        for i in range(minX, maxX):
            for j in range(minY, maxY):
                key = (i, j)
                if key not in self.layout_grid:
                    continue
                cell_list = self.layout_grid[key]
                for c in cell_list:
                    if c.id != randc.id:
                        overlap_sum += overlap_area(randc, c)
        return overlap_sum

    @staticmethod
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

    def clear(self):
        self.layout_grid.clear()

    def cleanup(self):
        self.c = None
        self.clear()
        for k in self.layout_grid.copy().keys():
            del self.layout_grid[k]
