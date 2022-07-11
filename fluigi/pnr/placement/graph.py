import matplotlib.pyplot as plt
import networkx as nx

import fluigi.parameters as parameters
from fluigi.pnr.hola import adaptagrams as adg
from fluigi.pnr.layout import Layout


def generatePlanarLayout(layout: Layout):
    positions = nx.planar_layout(layout.G)
    print("Positions for all the cells:", positions)
    print(positions)
    nx.draw(layout.G, positions)
    plt.show()
    plt.savefig("test.png")


def generateSpectralLayout(layout: Layout):
    positions = nx.spectral_layout(layout.G)
    print(positions)
    nx.draw(layout.G, positions)
    plt.show()

    positions = nx.planar_layout(layout.G)
    print(positions)
    nx.draw(layout.G, positions)
    plt.show()

    positions = nx.circular_layout(layout.G)
    print(positions)
    nx.draw(layout.G, positions)
    plt.show()

    positions = nx.bipartite_layout(layout.G, nx.bipartite.sets(layout.G)[0])
    print(positions)
    nx.draw(layout.G, positions)
    plt.show()

    positions = nx.shell_layout(layout.G)
    print(positions)
    nx.draw(layout.G, positions)
    plt.show()

    positions = nx.random_layout(layout.G)
    print(positions)
    nx.draw(layout.G, positions)
    plt.show()

    positions = nx.spiral_layout(layout.G)
    print(positions)
    nx.draw(layout.G, positions)
    plt.show()

    # plt.savefig('test.png')


def generateSpringLayout(layout: Layout):
    positions = nx.spring_layout(layout.G)
    print(positions)
    nx.draw(layout.G, positions)
    # plt.show()
    # plt.savefig('test.png')

    x_scale_factor = 0.7 * parameters.DEVICE_X_DIM / 2
    y_scale_factor = 0.7 * parameters.DEVICE_Y_DIM / 2

    center_x = parameters.DEVICE_X_DIM / 2
    center_y = parameters.DEVICE_Y_DIM / 2

    # Scale the positions based on the spring layout
    for cell_id in positions.keys():
        position = positions[cell_id]
        cell = layout.cells[cell_id]
        cell.x = int(center_x + position[0] * x_scale_factor)
        cell.y = int(center_y + position[1] * y_scale_factor)

    # Expand the components


def generateHOLALayout(layout: Layout):

    cell_node_map = dict()
    net_edge_map = dict()
    hola_graph = adg.Graph()

    # First convert layout into a dialect graph
    for cell_id in layout.cells.keys():
        cell = layout.cells[cell_id]
        print(cell)
        node = hola_graph.addNode()
        cell_node_map[cell] = node

    for net_id in layout.nets.keys():
        net = layout.nets[net_id]
        print(net)
        # Pull all the source and targets from the net
        source_id = net.source.component
        cell = layout.cells[source_id]

        source_node = cell_node_map[cell]

        for sink in net.sinks:
            sink_id = sink.component
            cell = layout.cells[sink_id]
            sink_node = cell_node_map[cell]
            edge = hola_graph.addEdge(source_node, sink_node)
            net_edge_map[net] = edge

    print("Before HOLA:")
    for cell in cell_node_map.keys():
        node_ref = cell_node_map[cell]
        bounding_box = node_ref.getBoundingBox()
        print("{}: x-{} y-{}".format(cell.ID, bounding_box.x, bounding_box.y))

    # This should basically do the layout
    adg.doHOLA(hola_graph)

    x_scale_factor = 0.007 * parameters.DEVICE_X_DIM / 2
    y_scale_factor = 0.007 * parameters.DEVICE_Y_DIM / 2

    center_x = parameters.DEVICE_X_DIM / 2
    center_y = parameters.DEVICE_Y_DIM / 2

    print("After HOLA:")
    for cell in cell_node_map.keys():
        node_ref = cell_node_map[cell]
        bounding_box = node_ref.getBoundingBox()
        print("Raw Version:")
        print("{}: x-{} y-{}".format(cell.ID, bounding_box.x, bounding_box.y))

        cell.x = int(center_x + bounding_box.x * x_scale_factor)
        cell.y = int(center_y + bounding_box.y * y_scale_factor)
        print("Scaled Version:")
        print("{}: x-{} y-{}".format(cell.ID, cell.x, cell.y))
