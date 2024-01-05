from __future__ import annotations

from enum import Enum

from tuple import Tuple 
from vertex import Vertex, Player
from liftstrategies import LiftStrategy, InputLiftStrategy, RandomLiftStrategy

class Strategy(Enum): 
    INPUT = 0 
    RANDOM = 1
    BACKTRACK = 2 
    LOOP = 3

def strategy_string(strategy: Strategy): 
    match strategy: 
        case Strategy.INPUT: 
            return "input order"
        case Strategy.RANDOM: 
            return "random order"
        case Strategy.BACKTRACK: 
            return "backtrack"
        case Strategy.LOOP: 
            return "loop elimination"

class ParityGame: 

    def __init__(self, n_vertices, file) -> None: 
        self.file = file
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
    
    def set_solve_strategy(self, strategy: Strategy): 
        self.strategy = strategy

    def __init_lift_strategy(self) -> LiftStrategy: 
        match self.strategy: 
            case Strategy.INPUT: 
                return InputLiftStrategy(self.vertices)
            case Strategy.RANDOM: 
                return RandomLiftStrategy(self.vertices)
            case Strategy.BACKTRACK: 
                return None 
            case Strategy.LOOP: 
                return None 

    # Solve parity game using small progress measures (SPM) algorithm
    def solve(self) -> None: 
        # Set empty tuples for each vertex 
        for v in self.vertices: 
            v.tuple = Tuple.get_empty_tuple()
            
        self.lift_amount = 0
        lift_strategy = self.__init_lift_strategy()
        while not self.__is_stable(self.vertices): 
            v: Vertex = lift_strategy.next_vertex()

            # lift the vertex 
            new_tuple: Tuple = self.__lift(v)
            self.lift_amount += 1
            # check if the found tuple is stable 
            v.stable = (new_tuple == v.tuple)
            # set the final tuple for the vertex 
            v.tuple = new_tuple

        self.print_results()
        
    def __is_stable(self, vertices: list[Vertex]): 
        for v in vertices: 
            if not v.stable: return False 
        return True 

    def __lift(self, v: Vertex): 
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
    
    def print_results(self): 
        odd_wins, even_wins = self.make_groups()
        print("##################################")
        print('File path:', self.file)
        print('Strategy:', strategy_string(self.strategy))
        print('Number of lifts:', self.lift_amount)
        print("Vertices that player odd wins:")
        print(odd_wins)
        print("Vertices that player even wins:")
        print(even_wins)
        print("##################################\n")

    def __str__(self) -> str:
        output_string = ''
        for vertex in self.vertices: 
            output_string += (str(vertex) + "\n")
        return output_string
       
