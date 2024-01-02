from __future__ import annotations
import os
import argparse

from graph import Graph

def get_files(path: str) -> (list[str], list[str]):
    files = os.listdir(path)
    graph_files = []
    query_files = []
    for file in files:
        if file.endswith('aut'):
            graph_files.append(file)
        elif file.endswith('mcf'):
            query_files.append(file)
    return (query_files, graph_files)

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="SPM parity game solver")
    # # Path to directory
    # parser.add_argument('dirpath', help='Path to directory')
    # If this is provided we don't run all the graph files
    parser.add_argument('-g', '--graph', help="Name of graph file to run")
    arguments = parser.parse_args()
    return arguments

def main():
    arguments = parse_arguments()
    graph = Graph.parse_graph(arguments.graph)
    print(graph)

if __name__ == "__main__": 
    main()
