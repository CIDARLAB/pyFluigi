import argparse
import io
import json
import os
import sys
import time
from os import system
from pathlib import Path

import networkx as nx
import pyfiglet
from pymint.mintdevice import MINTDevice

import fluigi.parameters as parameters
import fluigi.utils as utils
from fluigi.pnr.layout import Layout
from fluigi.pnr.placement.graph import (generateHOLALayout,
                                        generatePlanarLayout,
                                        generateSpectralLayout,
                                        generateSpringLayout)
from fluigi.pnr.placement.simulatedannealing import (
    generate_simulated_annealing_layout,
    generate_simulated_annealing_layout_v2)
from fluigi.pnr.terminalassignment import assign_single_port_terminals
from fluigi.primitives import pull_defaults, pull_dimensions, pull_terminals


def main():

    # parameters.PROGRAM_DIR = os.path.abspath(os.path.dirname(__file__))

    parser = argparse.ArgumentParser()

    parser.add_argument("input", help="This is the file thats used as the input ")
    parser.add_argument(
        "--outpath", type=str, default="out/", help="This is the output directory"
    )
    parser.add_argument(
        "-c",
        "--convert",
        action="store_true",
        help="Sets the flag to only convert the design and nothing else",
    )

    args = parser.parse_args()

    ascii_banner = pyfiglet.figlet_format("Fluigi")
    print(ascii_banner)

    print("output dir:", args.outpath)
    print("Running File: " + args.input)

    extension = Path(args.input).suffix
    if extension != ".mint" and extension != ".uf":
        print("Unrecognized file Extension")
        exit()

    abspath = Path(args.outpath).resolve()
    parameters.OUTPUT_DIR = abspath

    if os.path.isdir(abspath) is not True:
        print("Creating the output directory:")
        path = Path(parameters.OUTPUT_DIR)
        path.mkdir(parents=True)

    # Check if the device netlist is planar
    current_device = MINTDevice.from_mint_file(args.input)
    graph = current_device.G

    if nx.algorithms.check_planarity(graph) == False:
        print("Error - Non-planar graph seen")
        sys.exit(0)

    try:
        pull_defaults(current_device)
        pull_dimensions(current_device)
    except Exception as e:
        print("Error getting Primitive data: {}".format(e))

    layout = Layout()
    layout.importMINTwithoutConstraints(current_device)

    pull_defaults(current_device)
    pull_dimensions(current_device)
    pull_terminals(current_device)
    generateSpringLayout(layout)

    layout.applyLayout()

    tt = os.path.join(
        parameters.OUTPUT_DIR, "{}_no_par.json".format(current_device.name)
    )
    with open(tt, "w") as f:
        json.dump(current_device.to_parchmint_v1(), f)

    print(current_device.G.edges)

    utils.printgraph(current_device.G, current_device.name + ".dot")

    # We exit the process if only convert is set to true
    if args.convert:
        sys.exit(0)

    layout = Layout()
    layout.importMINTwithoutConstraints(current_device)

    # Do Terminal Assignment
    assign_single_port_terminals(current_device)

    # #Generate the Simulated Annealing Layout
    # generate_simulated_annealing_layout_v2(current_device)
    # generate_simulated_annealing_layout(layout)

    # generateSpectralLayout(layout)
    generateHOLALayout(layout)
    layout.applyLayout()
    layout.ensureLegalCoordinates()
    layout.print_layout()

    tt = os.path.join(
        parameters.OUTPUT_DIR, "{}_hola_par.json".format(current_device.name)
    )
    with open(tt, "w") as f:
        json.dump(current_device.to_parchmint_v1(), f)

    utils.printgraph(layout.G, current_device.name + ".layout.dot")


if __name__ == "__main__":
    main()
