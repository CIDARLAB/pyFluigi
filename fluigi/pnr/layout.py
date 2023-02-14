import sys
from enum import Enum
from math import floor
from typing import List, Optional

import cairo
import networkx as nx
from pymint.mintdevice import MINTDevice

from fluigi import parameters
from fluigi.parameters import PT_TO_UM
from fluigi.pnr.place_and_route import Cell as Obstacle
from fluigi.pnr.place_and_route import Net as CNet
from fluigi.pnr.place_and_route import PlacementCell as CCell
from fluigi.pnr.place_and_route import Placer as CPlacer
from fluigi.pnr.place_and_route import Route
from fluigi.pnr.place_and_route import Router as AARFRouter
from fluigi.pnr.place_and_route import Terminal as CTerminal
from fluigi.pnr.place_and_route import Vertex
from fluigi.pnr.sa.utils import get_terminal

# from fluigi.pnr.aarf import Cell as Obstacle
# from fluigi.pnr.aarf import Router as AARFRouter
# from fluigi.pnr.aarf import Vertex, Route


class RouterAlgorithms(Enum):
    AARF = 0
    GRID = 1


class PlaceAndRouteAlgorithms(Enum):
    PLANAR = 0
    SIMULATED_ANNEALING = 1


class Layout:
    def __init__(self) -> None:
        self.cells = dict()
        self.nets = dict()
        self.G = nx.MultiDiGraph()
        self.__original_device = None
        self.__direct_map = []

    def apply_layout(self):
        device = self.__original_device
        for ID in self.cells:
            component = device.get_component(ID)
            cell = self.cells[ID]
            component.params.set_param("position", [cell.x, cell.y])

        for ID in self.nets:
            connection = device.get_connection(ID)
            net = self.nets[ID]
            for route in net.routes:
                path = []
                for vertex in route.waypoints:
                    path.append((vertex.x, vertex.y))

                connection.add_waypoints_path(None, None, path)
                print("Updating connection: {} with path {}".format(connection.ID, str(path)))

    def ensureLegalCoordinates(self):
        # Make sure all the cell coordinates are positive
        minx = sys.maxsize
        miny = sys.maxsize
        maxx = -sys.maxsize
        maxy = -sys.maxsize

        for cell in [self.cells[id] for id in list(self.cells)]:
            if cell.x < minx:
                minx = cell.x
            if cell.x + cell.x_span > maxx:
                maxx = cell.x + cell.x_span

            if cell.y < miny:
                miny = cell.y
            if cell.y + cell.y_span > maxy:
                maxy = cell.y + cell.y_span

    def importMINTwithoutConstraints(self, device: MINTDevice) -> None:
        self.__original_device = device

        pcells = []

        for component in device.components:
            terminals = []
            for port in component.ports:
                t = CTerminal(
                    port.label,
                    floor(port.x / parameters.LAMBDA),
                    floor(port.y / parameters.LAMBDA),
                )
                print("Before Update: ({}, {})".format(t.x, t.y))
                t.compute_absolute_positions(
                    floor(component.xpos / parameters.LAMBDA),
                    floor(component.ypos / parameters.LAMBDA),
                )
                print("After Update: ({}, {})".format(t.x, t.y))

                terminals.append(t)

            if component.params.exists("componentSpacing"):
                component_spacing = component.params.get_param("componentSpacing")
            else:
                component_spacing = 5000  # Some random value
            pcell = CCell(
                component.ID,
                round(component.xpos / parameters.LAMBDA),
                round(component.ypos / parameters.LAMBDA),
                round(component.xspan / parameters.LAMBDA),
                round(component.yspan / parameters.LAMBDA),
                round(component_spacing / parameters.LAMBDA),
                terminals,
            )

            pcells.append(pcell)
            self.cells[pcell.id] = pcell

        for connection in device.connections:
            id = connection.ID
            source = self.cells[connection.source.component]
            source_terminal = None
            if connection.source.port is not None:
                # Get C Terminal for this
                try:
                    source_terminal = get_terminal(source, connection.source.port)
                    # source_terminal = source.get_terminal(connection.source.port)
                except Exception:
                    print(
                        "Could not find Terminal for source port: {} {} for connection: {}".format(
                            source.id, connection.source.port, id
                        )
                    )
            else:
                if len(source.ports) == 1:
                    print('Assigning "1" as the default terminal for net')
                    # source_terminal = get_terminal(source, "1")
                    source_terminal = source.ports[0]
                else:
                    raise Exception(
                        "No scheme for handling scenarios where no source port is defined and there's more than 1 port available"
                    )
                    source_terminal = None

            sink_cells = []
            sink_terminals = []
            for sink in connection.sinks:
                pcell = self.cells[sink.component]
                sink_cells.append(pcell)
                if sink.port is not None:
                    try:
                        t = get_terminal(pcell, sink.port)
                        sink_terminals.append(t)
                    except Exception:
                        print("Could not find Terminal for source port: {} for connection: {}".format(source.id, id))

                else:
                    if len(pcell.ports) == 1:
                        print('Assigning "1" as the default terminal for net')
                        # t = get_terminal(pcell, "1")
                        t = pcell.ports[0]
                        sink_terminals.append(t)
                    else:
                        raise Exception(
                            "No scheme for handling scenarios where no source port is defined and there's more than 1 port available"
                        )
                        sink_terminals.append(None)

            # cnet.sinks = sink_cells
            # cnet.sink_terminals = sink_terminals

            cnet = CNet()
            cnet.id = id
            cnet.source = source
            cnet.source_terminal = source_terminal

            width = connection.params.get_param("channelWidth")
            cnet.channelWidth = width

            spacing = 2 * width
            cnet.channelSpacing = spacing

            # TODO - Figure out how to fix the interface later
            for sink_cell in sink_cells:
                cnet.sinks.append(sink_cell)

            # TODO - Figure out how to fix the interface later
            for sink_terminal in sink_terminals:
                cnet.sink_terminals.append(sink_terminal)

            self.nets[cnet.id] = cnet

    def importMINTwithConstraints(self, device: MINTDevice) -> None:
        # TODO: Process the constraints
        raise Exception("Not Implemented")

    def route_nets(self, router_type: RouterAlgorithms = RouterAlgorithms.AARF) -> None:
        # Step 1 - generate the source and targets points for all the connections
        all_routes = []
        obstacle_check_vertices = []
        for net in list(self.nets.values()):
            # Just get a single source and sink
            source_vertex = Vertex()

            source_vertex.x = net.source_terminal.x
            source_vertex.y = net.source_terminal.y

            obstacle_check_vertices.append(source_vertex)

            for sink_terminal in net.sink_terminals:
                target_vertex = Vertex()
                target_vertex.x = sink_terminal.x
                target_vertex.y = sink_terminal.y

                obstacle_check_vertices.append(target_vertex)

                route = Route(
                    net.id,
                    source_vertex,
                    target_vertex,
                    net.channelWidth,
                    net.channelSpacing,
                )
                # r = Route(net.ID, source_vertex, target_vertex)
                all_routes.append(route)

                # TODO - FIX THIS LATER
                net.routes.append(route)

        obstacles = []
        # Step 2 - generate the obstacles from the components
        for ID, cell in list(self.cells.items()):
            # TODO - CHECK IF ANY OF THE ROUTES HAVE THESE AS THE INPUTS/OUTPUTS
            overlaps_vertex = False
            for vertex in obstacle_check_vertices:
                overlaps_vertex = overlaps_vertex or inside_obstabcle(vertex, cell)
                if overlaps_vertex:
                    break
            if overlaps_vertex is False:
                obstacle = Obstacle()
                obstacle.x = cell.x + 1
                obstacle.y = cell.y + 1
                obstacle.x_span = cell.x_span - 1
                obstacle.y_span = cell.y_span - 1
                obstacles.append(obstacle)

        # Step 3 - Do the routing
        router = AARFRouter(obstacles)
        router.route(all_routes, 0, 0, parameters.DEVICE_X_DIM, parameters.DEVICE_Y_DIM)

        # TODO - New API
        # router = AARFRouter(obstacles)
        # router.route(routes)

        print(all_routes)
        print("Routed route:")
        for route in all_routes:
            print(
                "Route: Start - ({}, {}) End - ({}, {})".format(route.start.x, route.start.y, route.end.x, route.end.y)
            )
            print("Waypoints:")
            for waypoint in route.waypoints:
                print("({}, {})".format(waypoint.x, waypoint.y))

    def place_and_route_design(self):
        cells = list(self.cells.values())
        nets = list(self.nets.values())
        constraints = []
        placer = CPlacer(cells, nets, constraints)
        placer.place(parameters.DEVICE_X_DIM, parameters.DEVICE_Y_DIM)
        placer.place_and_route()

    def print_layout(self, postfix: str = "") -> None:
        xspan = parameters.DEVICE_X_DIM
        yspan = parameters.DEVICE_Y_DIM

        if postfix != "":
            filename = "{}_{}.svg".format(self.__original_device.name, postfix)
        else:
            filename = "{}.svg".format(self.__original_device.name)

        filepath = parameters.OUTPUT_DIR.joinpath(filename)

        print("Generating the SVG preview")
        surface = cairo.SVGSurface(
            str(filepath),
            xspan * PT_TO_UM,
            yspan * PT_TO_UM,
        )

        ctx = cairo.Context(surface)
        ctx.scale(PT_TO_UM, PT_TO_UM)

        for cell in self.cells.values():
            ctx.rectangle(cell.x, cell.y, cell.x_span, cell.y_span)
            ctx.fill()

        for net in self.nets.values():
            for route in net.routes:
                waypoints = route.waypoints
                for i in range(len(route.waypoints) - 1):
                    waypoint = waypoints[i]
                    next_waypoint = waypoints[i + 1]
                    ctx.move_to(waypoint.x, waypoint.y)
                    ctx.line_to(next_waypoint.x, next_waypoint.y)
                    ctx.set_line_width(route.channelWidth / 2)
                    ctx.stroke()

        surface.finish()


def inside_obstabcle(vertex: Vertex, obstacle: CCell) -> bool:
    if (
        vertex.x >= obstacle.x
        and vertex.x <= obstacle.x + obstacle.x_span
        and vertex.y >= obstacle.y
        and vertex.y <= obstacle.y + obstacle.y_span
    ):
        return True
    else:
        return False
