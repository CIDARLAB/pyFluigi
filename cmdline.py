from primitives import pull_defaults, pull_dimensions
from pnr.layout import Layout
import sys
import os
from pathlib import Path
import time
from antlr4 import CommonTokenStream, ParseTreeWalker, FileStream
import argparse
import parameters
import json
import utils
import networkx as nx

from pyMINT.antlr.mintLexer import mintLexer
from pyMINT.antlr.mintParser import mintParser
from pyMINT.mintcompiler import MINTCompiler

from pnr.placement.graph import generatePlanarLayout, generateSpectralLayout, generateSpringLayout


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'input', help="This is the file thats used as the input ")
    parser.add_argument('--outpath', type=str, default="out/",
                        help="This is the output directory")

    args = parser.parse_args()
    print("output dir:", args.outpath)
    print("Running File: "+args.input)

    extension = Path(args.input).suffix
    if extension != '.mint' and extension != '.uf' :
        print("Unrecognized file Extension")
        exit()

    abspath = os.path.abspath(args.outpath)
    parameters.OUTPUT_DIR = abspath

    if os.path.isdir(abspath) is not True:
        print("Creating the output directory:")
        path = Path(parameters.OUTPUT_DIR)
        path.mkdir(parents=True)

    finput = FileStream(args.input)

    lexer = mintLexer(finput)

    stream = CommonTokenStream(lexer)

    parser = mintParser(stream)

    tree = parser.netlist()

    walker = ParseTreeWalker()

    listener = MINTCompiler()

    walker.walk(listener, tree)

    #Check if the device netlist is planar
    graph = listener.current_device.G


    if nx.algorithms.check_planarity(graph) == False:
        print('Error - Non-planar graph seen')
        sys.exit(0)



    current_device = listener.current_device

    pull_defaults(listener.current_device)
    pull_dimensions(listener.current_device)


    tt = os.path.join(parameters.OUTPUT_DIR, '{}_no_par.json'.format(current_device.name))
    with open(tt, 'w') as f:
        json.dump(current_device.toParchMintV1(), f)

    print(listener.current_device.G.edges)
    utils.printgraph(listener.current_device.G, current_device.name+'.dot')

    layout = Layout()
    layout.importMINTwithoutConstraints(current_device)
    
    generateSpectralLayout(layout)

    utils.printgraph(layout.G, current_device.name+'.layout.dot')



if __name__ == "__main__":
    main()
