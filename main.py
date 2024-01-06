from __future__ import annotations
import os
import argparse

from paritygame import ParityGame, Strategy

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="SPM parity game solver")
    parser.add_argument('-pg', '--paritygame', help="Path + name to the paritygame file")
    arguments = parser.parse_args()
    return arguments

def main():
    arguments = parse_arguments()
    paritygame = ParityGame.parse_graph(arguments.paritygame)
    paritygame.set_solve_strategy(Strategy.BACKTRACK)
    paritygame.solve()
    
if __name__ == "__main__": 
    main()
