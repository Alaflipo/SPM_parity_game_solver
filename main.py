from __future__ import annotations
import argparse

from paritygame import ParityGame, Strategy, strategy_string

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="SPM parity game solver")
    parser.add_argument('-pg', '--paritygame', help="Path + name to the paritygame file")
    parser.add_argument('-s', '--strategy', help="choose from: input, random, selfloop, backtrack or combined")
    arguments = parser.parse_args()
    return arguments

def solve_every_strat(pg: ParityGame): 
    for strat in Strategy: 
        pg.set_solve_strategy(strat)
        pg.solve()

def main():
    arguments = parse_arguments()
    paritygame = ParityGame.parse_graph(arguments.paritygame)
    paritygame.set_solve_strategy(arguments.strategy)
    paritygame.solve()
    
if __name__ == "__main__": 
    main()
