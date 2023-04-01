from typing import List
import networkx as nx
from pymint import MINTDevice

# Step 1 - Trim the graph of the design (Based on how hola does it) - Keep the stem add the leaves in the ignore list
# Step 2 - Find the source nodes (traverse level by level for each).
# Step 3 - Assume positions to be checkerboard-esque. Center of stem has 0.
# Step 4 - Traverse each of the nodes (Breadth First , pick heaviest stem node first). based on the location of the source port decide North, East, South, West. and place the next component based on that. Basically, always go east (1 neighbour) North/South/pure East if there are (2 / more neighbours on the stem)
# Step 4.5 - Modify the rotation of the newly placed component to reduce the distance between source and sink ports
# Step 5 -  Component expansion


def step_1_1(
    device: MINTDevice,
    stem_graph,
    leaves: List[str],
    start_list: List[str],
):

    # Step 1.1 - Trim the graph of the design (Based on how hola does it) - Keep the stem add the leaves in the ignore list

    # Find the leaves
    for node in stem_graph.nodes:
        if (
            len(list(stem_graph.successors(node))) == 0
            and len(list(stem_graph.predecessors(node))) == 1
        ):
            leaves.append(node)
        elif (
            len(list(stem_graph.successors(node))) == 1
            and len(list(stem_graph.predecessors(node))) == 0
        ):
            leaves.append(node)

    # Remove the leaves from the stem graph
    for leaf in leaves:
        stem_graph.remove_node(leaf)

    # Step 2 - Find the source nodes (traverse level by level for each).

    # Find the start list for traversing level by level
    for node in stem_graph.nodes:
        if len(list(stem_graph.predecessors(node))) == 0:
            start_list.append(node)


def step_1_2(
    device: MINTDevice,
    stem_graph,
    leaves: List[str],
    start_list: List[str],
) -> List[List[str]]:
    # Generate all the levels we need to traverse in the stem graph Levels is a list of lists that has the onde reference for every node in that particular level
    levels = [[]]
    level_index = 0
    traversed_nodes = []

    # Added all the start list nodes to the first level
    for node in start_list:
        levels[level_index].append(node)
        # add to traversed nodes
        traversed_nodes.append(node)

    # Traverse the stem graph level by level
    # Loop till all nodes in the stem graph are traversed
    while set(stem_graph.nodes) != set(traversed_nodes):
        # Find the successors of the nodes in the current level
        level_nodes = []
        for node in levels[-1]:
            for successor in stem_graph.successors(node):
                if successor not in traversed_nodes:
                    level_nodes.append(successor)
                    traversed_nodes.append(successor)
        levels.append(level_nodes)

    return levels
