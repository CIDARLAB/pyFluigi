from pymint.mintdevice import MINTDevice
import pnr.dropx.step1 as step1
import pnr.dropx.step2 as step2
import pnr.dropx.step3 as step3
import pnr.dropx.step4 as step4


def place_and_route_dropx(device: MINTDevice) -> None:
    # Make a copy mint device graph
    stem_graph = device.G.copy()

    leaves = []
    start_list = []
    step1.step_1_1(device, stem_graph, leaves, start_list)
    levels = step1.step_1_2(device, stem_graph, leaves, start_list)
    print("All the Levels:", levels)
    dfs_chains = step2.step_2_1(stem_graph, levels)
    print("All the DFS Chains:", dfs_chains)
    step2.step_2_2(stem_graph, levels, dfs_chains)
    print("positions: ", step2.POSITION_MAP)
    # Step 2.3: Y-Shift all the dfs chains in the radiating patterns
    step2.step_2_3(stem_graph, levels, dfs_chains)
    print("positions: ", step2.POSITION_MAP)

    # Step 3: Fix all the rotations of the components in the dfs chains
    step3.step_3_1(device, stem_graph, levels, dfs_chains)
    print("positions: ", step2.POSITION_MAP)

    # Step 4: Add all the leaves back to the stem graph and do the respective x and y shifts
    step4.step_4_1(device, stem_graph, levels, dfs_chains)
    print("positions: ", step2.POSITION_MAP)
    # Step 5: Do the compnent expansion for all the components
    print("positions: ", step2.POSITION_MAP)
    # Step 6: Do the routing
    print("positions: ", step2.POSITION_MAP)
    # Step 7: Center the design onto the canvas and add paddings
    print("positions: ", step2.POSITION_MAP)
