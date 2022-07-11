from __future__ import annotations

import random
import sys
import time
from math import exp, floor

import numpy

from fluigi.parameters import (
    DEFAULT_MOVES_PER_TEMP_PER_MODULE,
    DEVICE_X_DIM,
    DEVICE_Y_DIM,
    LAMBDA,
    SIGMA_MULTIPLIER,
)
from fluigi.pnr.sa.salayout import SALayout
from fluigi.pnr.sa.utils import (
    AlgDataStorage,
    select_random_component,
    storage,
    update_terminals,
)


class SAPlace:
    def __init__(self, salayout: SALayout) -> None:
        super().__init__()
        random.seed(time.time_ns())
        self.layout = salayout
        self.list_components = list(salayout.cells.values())
        self.seed = 0
        # list_components = []
        self.rate_accept = 0.0
        self.temp = 0
        self.range_x = DEVICE_X_DIM / LAMBDA
        self.range_y = DEVICE_Y_DIM / LAMBDA
        self.initial_temp = sys.maxsize

    def cleanup(self) -> None:
        self.reset()
        self.list_components = []
        layout = None

    def reset(self) -> None:
        self.layout.clear()

    def place(self) -> None:
        self.init_place()
        self.init_temp()
        temp = self.initial_temp

        while (
            temp >= 0.005 * self.layout.cur_cost / len(self.list_components)
            and self.layout.cur_cost > 2
        ):
            for i in range(
                len(self.list_components) * DEFAULT_MOVES_PER_TEMP_PER_MODULE
            ):
                # TODO - Shouldnt this be a random component
                randc = self.list_components[i % len(self.list_components)]
                if random.random() > 0.5:
                    randx = int(self.range_x / 2 * random.random())
                else:
                    randx = -int(self.range_x / 2 * random.random())

                if random.random() > 0.5:
                    randy = int(self.range_y / 2 * random.random())
                else:
                    randy = -int(self.range_y / 2 * random.random())

                if random.random() > 0.5:
                    randx = 0
                else:
                    randy = 0

                self.layout.calc_prev_comp_overlap(randc)
                self.layout.calc_prev_comp_wirelength(randc)
                self.layout.grid.new_move(randc, randx, randy)
                self.layout.calculate_cost(randc)

                test = random.random()
                if self.layout.get_delta_cost() <= 0:
                    self.layout.grid.apply_move()
                    self.rate_accept += 1.0
                elif test < exp(-(self.layout.get_delta_cost() / temp)):
                    self.layout.grid.apply_move()
                    self.rate_accept += 1.0
                else:
                    self.layout.grid.undo_move()
                    self.layout.undo_update_cost()

            self.rate_accept = self.rate_accept / float(
                len(self.list_components) * DEFAULT_MOVES_PER_TEMP_PER_MODULE
            )

            self.range_x = int(floor(self.range_x) * (1.0 - 0.44 + self.rate_accept))
            self.range_y = int(floor(self.range_y) * (1.0 - 0.44 + self.rate_accept))

            if self.range_x >= DEVICE_X_DIM / LAMBDA:
                self.range_x = DEVICE_X_DIM / LAMBDA

            if self.range_y >= DEVICE_Y_DIM / LAMBDA:
                self.range_y = DEVICE_Y_DIM / LAMBDA

            if self.rate_accept > 0.96:
                temp = 0.5 * temp
            elif self.rate_accept <= 0.96 and self.rate_accept > 0.8:
                temp = 0.9 * temp
            elif self.rate_accept <= 0.8 and self.rate_accept > 0.15:
                temp = 0.95 * temp
            else:
                temp = 0.8 * temp
            print("-> Temp = {}".format(temp))

        print("Final Temp = {}".format(temp))
        print("Overlap = {}".format(self.layout.calculate_overlap()))

    def init_place(self):
        print("Initializing Simulated Annealing Placer...")
        for cell in self.list_components:
            rand_x = int(self.range_x * random.random())
            rand_y = int(self.range_y * random.random())
            cell.x = rand_x
            cell.y = rand_y
            update_terminals(cell)
            self.layout.grid.add_component(cell)
        self.layout.calculate_init_cost()

    def init_temp(self):
        print("Initializing Temperature...")
        # storage.store_data("Current Top Edge", self.layout.cur_top_edge)
        # storage.store_data("Current Right Edge", self.layout.cur_right_edge)
        # storage.store_data("Current Bottom Edge", self.layout.cur_bottom_edge)
        # storage.store_data("Current Left Edge", self.layout.cur_left_edge)

        # storage.store_data("Old Cost", self.layout.old_cost)
        # storage.store_data("Old Area", self.layout.old_area)
        # storage.store_data("Old Overlap", self.layout.old_overlap)
        # storage.store_data("Old wirelength", self.layout.old_wirelength)

        # storage.store_data("Current Cost", self.layout.cur_cost)
        # storage.store_data("Current Area", self.layout.cur_area)
        # storage.store_data("Current Overlap", self.layout.cur_overlap)
        # storage.store_data("Current Wirelength", self.layout.cur_wirelength)

        # storage.store_data(
        #     "Previous move comp overlap", self.layout.pre_move_comp_overlap
        # )
        # storage.store_data("Previous move wirelength", self.layout.pre_move_wirelength)
        # storage.store_data("Final cost", self.layout.cur_cost)
        # storage.new_stage()
        cost_history = []
        for i in range(len(self.list_components)):
            if random.random() > 0.5:
                rand_x = int(self.range_x / 2 * random.random())
            else:
                rand_x = int(-self.range_x / 2 * random.random())

            if random.random() > 0.5:
                rand_y = int(self.range_y / 2 * random.random())
            else:
                rand_y = int(-self.range_y / 2 * random.random())

            rand_c = select_random_component(self.list_components)
            print("Moving random component: {}".format(rand_c.id))
            self.layout.calc_prev_comp_wirelength(rand_c)
            self.layout.grid.new_move(rand_c, rand_x, rand_y)
            self.layout.grid.apply_move()
            self.layout.calculate_cost(rand_c)
            cost_history.append(self.layout.cur_cost)
            # storage.store_data("Current Top Edge", self.layout.cur_top_edge)
            # storage.store_data("Current Right Edge", self.layout.cur_right_edge)
            # storage.store_data("Current Bottom Edge", self.layout.cur_bottom_edge)
            # storage.store_data("Current Left Edge", self.layout.cur_left_edge)

            # storage.store_data("Old Cost", self.layout.old_cost)
            # storage.store_data("Old Area", self.layout.old_area)
            # storage.store_data("Old Overlap", self.layout.old_overlap)
            # storage.store_data("Old wirelength", self.layout.old_wirelength)

            # storage.store_data("Current Cost", self.layout.cur_cost)
            # storage.store_data("Current Area", self.layout.cur_area)
            # storage.store_data("Current Overlap", self.layout.cur_overlap)
            # storage.store_data("Current Wirelength", self.layout.cur_wirelength)

            # storage.store_data(
            #     "Previous move comp overlap", self.layout.pre_move_comp_overlap
            # )
            # storage.store_data(
            #     "Previous move wirelength", self.layout.pre_move_wirelength
            # )
            # storage.store_data("Final cost", self.layout.cur_cost)

        self.initial_temp = SIGMA_MULTIPLIER * numpy.std(cost_history)
        print("Initial Temperature: {}".format(self.initial_temp))
        # storage.print_data()
        storage.save_data()
