from __future__ import annotations

from enum import Enum

from tuple import Tuple 
from vertex import Vertex, Player
from liftstrategies import LiftStrategy, InputLiftStrategy, RandomLiftStrategy, BackTrackLiftStrategy, SelfLoopStrategy, OddFirstBackTrackSelfLoopStrategy

class Strategy(Enum): 
    INPUT = 0 
    RANDOM = 1
    BACKTRACK = 2 
    LOOP = 3
    LOOPBACKTRACKODD = 4

def strategy_string(strategy: Strategy): 
    match strategy: 
        case Strategy.INPUT: 
            return "input"
        case Strategy.RANDOM: 
            return "random"
        case Strategy.BACKTRACK: 
            return "backtrack"
        case Strategy.LOOP: 
            return "loop elim"
        case Strategy.LOOPBACKTRACKODD: 
            return "loop elim + backtrack"

def string_to_strat(strat_str: str): 
    match strat_str: 
        case "input": 
            return Strategy.INPUT
        case "random": 
            return Strategy.RANDOM
        case "backtrack": 
            return Strategy.BACKTRACK
        case "selfloop": 
            return Strategy.LOOP
        case "combined": 
            return Strategy.LOOPBACKTRACKODD

class ParityGame: 

    def __init__(self, n_vertices, file) -> None: 
        self.file: str = file
        self.n_vertices: int = n_vertices
        self.vertices: list[Vertex] = [Vertex(id=i) for i in range(n_vertices)]
        self.max_priority: int = -1

        self.strategy: Strategy = Strategy.INPUT
        self.lift_amount: int = 0 

    @staticmethod
    def parse_graph(filepath: str) -> ParityGame: 
        # read file 
        with open(filepath, 'r') as file:
            lines = file.read().strip().split('\n')

        # parse header info and create graph with vertices
        pg = ParityGame(int(lines[0].strip(";").split(" ")[1]) + 1, filepath)
        
        # Parse info for each vertex
        for i in range(1, len(lines)):
            vertex_info = lines[i].strip(";").split(' ')
            pg.vertices[int(vertex_info[0])].parse_vertex(
                vertex_info=vertex_info, 
                other_vertices=pg.vertices)
            
            # Set max priority 
            if (pg.vertices[int(vertex_info[0])].priority > pg.max_priority): 
                pg.max_priority = pg.vertices[int(vertex_info[0])].priority

        # Set the maximum tuple
        pg.__set_max_tuple()

        return pg
    
    # Sets the maximum tuple rho can become 
    def __set_max_tuple(self): 
        Tuple.set_tuple_size(self.max_priority + 1)
        Tuple.set_max_tuple([v.priority for v in self.vertices])
    
    def set_solve_strategy(self, strategy_str: str): 
        self.strategy = string_to_strat(strategy_str)

    def __init_lift_strategy(self) -> LiftStrategy: 
        match self.strategy: 
            case Strategy.INPUT: 
                return InputLiftStrategy(self.vertices)
            case Strategy.RANDOM: 
                return RandomLiftStrategy(self.vertices)
            case Strategy.BACKTRACK: 
                return BackTrackLiftStrategy(self.vertices)
            case Strategy.LOOP: 
                return SelfLoopStrategy(self.vertices) 
            case Strategy.LOOPBACKTRACKODD: 
                return OddFirstBackTrackSelfLoopStrategy(self.vertices)
    
    def __reset_vertices(self): 
        # Set empty tuples for each vertex and reset stability measure
        for v in self.vertices: 
            v.stable = False 
            v.tuple = Tuple.get_empty_tuple()

    # Solve parity game using small progress measures (SPM) algorithm
    def solve(self) -> None: 
        # reset vertices
        self.__reset_vertices()
        
        # set lfiting startegy generator
        self.lift_amount = 0
        lift_strategy = self.__init_lift_strategy()

        while not self.__is_stable(self.vertices): 
            v: Vertex | None = lift_strategy.next_vertex()
            if not v: break # if the queue is empty we break out of the loop

            # lift the vertex 
            new_tuple: Tuple = self.__lift(v)
            self.lift_amount += 1
            # check if the found tuple is stable 
            if (new_tuple == v.tuple): 
                # no change in tuple 
                v.stable = True 
            else: 
                # there has been a change in tuple 
                v.stable = False 
                lift_strategy.was_lifted(v)
            # set the final tuple for the vertex 
            v.tuple = new_tuple

        self.print_results()
        
    def __is_stable(self, vertices: list[Vertex]): 
        for v in vertices: 
            if not v.stable: return False 
        return True 

    def __lift(self, v: Vertex) -> Tuple: 
        if (v.owner == Player.EVEN): 
            # initilize the tuple to the largest tuple (top)
            min_tup: Tuple = Tuple.get_empty_tuple() 
            min_tup.set_top(True)

            for w in v.next: 
                new_tup: Tuple = self.__prog(v, w)
                # less then 
                if new_tup < min_tup: 
                    min_tup = new_tup
            return v.tuple if v.tuple > min_tup else min_tup
        else: 
            # initilize the tuple to the smallest tuple 
            max_tup: Tuple = Tuple.get_empty_tuple() 

            for w in v.next: 
                new_tup: Tuple = self.__prog(v,w)
                # greater then 
                if new_tup > max_tup: 
                    max_tup = new_tup 
            return v.tuple if v.tuple > max_tup else max_tup

    def __prog(self, v: Vertex, w: Vertex): 
        m: Tuple = Tuple.get_empty_tuple()
        if (w.tuple.top):
            m.set_top(True)

        if (v.even_priority): 
            # always set it equal to the smallest option 
            m.set_value_range(0, v.priority + 1, w.tuple.get_range(0, v.priority + 1))
        else: 
            m.set_value_range(0, v.priority + 1, w.tuple.get_range(0, v.priority + 1))
            m.add(v.priority)
        return m 
    
    def make_groups(self) -> tuple[list[Vertex], list[Vertex]]: 
        odd_wins: list[Vertex] = []
        even_wins: list[Vertex] = []
        for v in self.vertices: 
            if v.tuple.top: 
                odd_wins.append(v)
            else: 
                even_wins.append(v)
        return odd_wins, even_wins 
    
    def print_results(self) -> None: 
        odd_wins, even_wins = self.make_groups()
        print("##################################")
        print('File path:', self.file)
        print('Strategy:', strategy_string(self.strategy))
        print('Number of lifts:', self.lift_amount)
        print("Vertices that player odd wins:", len(odd_wins))
        print("Vertices that player even wins:", len(even_wins))
        print("Verdict:", "odd wins" if self.vertices[0].tuple.top else "even wins")
        print("##################################\n")

    def __str__(self) -> str:
        output_string = ''
        for vertex in self.vertices: 
            output_string += (str(vertex) + "\n")
        return output_string
       
