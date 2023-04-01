from typing import Dict, List, Tuple
import networkx as nx

# Step 3 - Assume positions to be checkerboard-esque. Center of stem has 0.
# Step 4 - Traverse each of the nodes (Breadth First , pick heaviest stem node first). based on the location of the source port decide North, East, South, West. and place the next component based on that. Basically, always go east (1 neighbour) North/South/pure East if there are (2 / more neighbours on the stem)
# Step 4.5 - Modify the rotation of the newly placed component to reduce the distance between source and sink ports
# Step 5 -  Component expansio

START_LOCATION_X = 0
START_LOCATION_Y = 0

POSITION_MAP: Dict[str, Tuple[int, int]] = {}


# def step_2_1(stem_graph, levels):
#     # Loop through each of the levels
#     location_y = START_LOCATION_Y
#     location_x = START_LOCATION_X
#     for level in levels:
#         # Find the size of the level
#         level_size = len(level)
#         # If the level sie is odd, then shift the start y location to rounded down half of the level size
#         if is_odd(level_size):
#             location_y = int((level_size - 1) / 2)
#         else:
#             location_y = int(level_size / 2)

#         # Set the positions of all the components in the level and save it into position map
#         for component in level:
#             postition_map[component] = (location_x, location_y)
#             location_y += 1
#             if is_odd(level_size) is False and location_y == 0:
#                 location_y = 1

#         # Now that the level is done, lets increment it
#         location_x += 1


def is_odd(level_size):
    return level_size % 2 == 1


def get_radiating_pattern_index(index, level_size) -> int:
    location_y = index
    if is_odd(level_size):
        location_y = int((location_y - 1) / 2)
    else:
        location_y = int(location_y / 2)

    if location_y == 0:
        return 0

    if is_odd(location_y):
        return int(-(location_y + 1) / 2)
    return int(location_y / 2)


def step_2_1(stem_graph, levels):
    # Set the y locations of all the components in step 1

    # Find the which node in level 1 with the largest DFS chain and sort them in decending order
    first_level = levels[0]
    dfs_chains = []

    # Find all the DFS chains and sort them in decending order
    for component in first_level:
        dfs_chain = list(nx.dfs_preorder_nodes(stem_graph, source=component))
        dfs_chains.append(dfs_chain)
    dfs_chains.sort(key=lambda x: len(x), reverse=True)

    # Go down the DFS chains and set ypositions radiating out from 0
    i = 0 if is_odd(len(first_level)) else 1
    for dfs_chain in dfs_chains:
        # Get the souce node
        souce_node = dfs_chain[0]
        # Get the y position of the source node
        y_position = get_radiating_pattern_index(i, len(first_level))
        # Set the y position of the source node
        POSITION_MAP[souce_node] = (0, y_position)

    # Returns the dfs chains
    return dfs_chains


def step_2_2(stem_graph, levels, dfs_chains):
    # Go though each of the dfs chains
    for dfs_chain in dfs_chains:
        # Loop through each of the levels
        for i in range(len(levels)):
            # Get the level
            level = levels[i]
            # Pattern index
            pattern_index = 0
            # Get the level node
            for level_node in level:
                # If the level node is in the DFS chain
                if level_node in dfs_chain:
                    # Get the y position of the level node
                    y_position = get_radiating_pattern_index(pattern_index, len(level))
                    # Set the y position of the level node
                    POSITION_MAP[level_node] = (
                        i,
                        y_position,
                    )
                    # Increment the pattern index
                    pattern_index += 1


def step_2_3(stem_graph, levels: List[List[str]], dfs_chains: List[List[str]]):
    # Go though each of the dfs chains, and then Y Shift based on the radiating pattern index
    main_y_offset_multiplier = 0
    for i in range(len(dfs_chains)):
        # Get the dfs chain
        dfs_chain = dfs_chains[i]
        # Get main offset
        main_y_offset_multiplier = get_radiating_pattern_index(i, len(dfs_chains))
        # Loop through each of the levels and shift the y position of the level nodes based on the radiating pattern index
        for level in levels:
            # Find out which dfs chain nodes are in this level
            level_dfs_chain_nodes = [node for node in level if node in dfs_chain]
            # Loop through each of the level nodes
            for j in range(len(level_dfs_chain_nodes)):
                level_node = level_dfs_chain_nodes[j]
                # Get the y position of the level node
                y_position = get_radiating_pattern_index(j, len(level_dfs_chain_nodes))
                # Set the y position of the level node
                POSITION_MAP[level_node] = (POSITION_MAP[level_node][0], y_position)
