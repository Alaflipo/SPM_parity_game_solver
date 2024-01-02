from __future__ import annotations

from enum import Enum

class Color(Enum):
    ODD = 1
    EVEN = 2

class Vertex: 

    def __init__(self, id: int) -> None: 
        self.id: int = id
        self.name: str = ""
        self.priority: int = 0
        self.owner: Color = Color.EVEN
        self.next: set[Vertex] = set()
        self.prev: set[Vertex] = set()

    def parse_vertex(self, vertex_info: str, other_vertices: list[Vertex]) -> None: 
        self.priority = int(vertex_info[1])
        self.owner = int(vertex_info[2])
        for next_id in vertex_info[3].split(','): 
            self.add_transition(other_vertices[int(next_id)])
        self.name = " ".join(vertex_info[4:]).strip("\"") if len(vertex_info) > 4 else ''
    
    def add_transition(self, other: Vertex) -> None: 
        self.next.add(other)
        other.prev.add(self)
    
    def __str__(self) -> str: 
        return "{id} ({name}): {transitions}".format(id=self.id, name=self.name, transitions=self.next)

    def __repr__(self) -> str:
        return str(self.id)

class Graph: 

    def __init__(self, n_vertices) -> None: 
        self.n_vertices: int = n_vertices
        self.vertices: list[Vertex] = [Vertex(id=i) for i in range(n_vertices)]

    @staticmethod
    def parse_graph(filepath: str) -> Graph: 
        # read file 
        with open(filepath, 'r') as file:
            lines = file.read().strip().split('\n')
            print(lines)

        # parse header info and create graph with vertices
        graph = Graph(int(lines[0].strip(";").split(" ")[1]) + 1)
        
        # Parse info for each vertex
        for i in range(1, len(lines)):
            vertex_info = lines[i].strip(";").split(' ')
            graph.vertices[int(vertex_info[0])].parse_vertex(
                vertex_info=vertex_info, 
                other_vertices=graph.vertices)
        return graph

    def __str__(self) -> str:
        output_string = ''
        for vertex in self.vertices: 
            output_string += (str(vertex) + "\n")
        return output_string
       
