from typing import List, Union
from parchmint.device import Device
import networkx as nx
from pymint.mintdevice import MINTDevice
from fluigi.pnr.dropx.step2 import POSITION_MAP


def assign_relative_position(
    device: Union[MINTDevice, Device], stem_node: str, leaf_node: str
) -> None:

    # Get the connection between the leaf component and the stem component
    device.get_connection_between_components(stem_node, leaf_node)


def step_4_1(
    device: Union[MINTDevice, Device],
    stem_graph,
    levels: List[List[str]],
    dfs_chains: List[List[str]],
) -> None:

    # generate positions for all the leaf components based on whether they are on the bottom or top of the component

    # Go through each of the DFS chains and find the component that is not a part of the stem graph
    for dfs_chain in dfs_chains:
        for node in device.G.nodes:

            # Skip if not in the stem graph
            if node not in dfs_chain:
                continue

            # Find all connecting node in the stem graph
            connected_nodes = list(stem_graph.neighbors(node))
            print("Nodes connected to {}: {}".format(node, connected_nodes))

            connected_node = connected_nodes[0]
            # Figure out the relative position of connected node to the DFS chain
            pos_connected_node = POSITION_MAP[connected_node]

            assign_relative_position(device, connected_node, node)
