from __future__ import annotations

from enum import Enum

from tuple import Tuple 

class Player(Enum):
    ODD = 0
    EVEN = 1

class Vertex: 

    def __init__(self, id: int) -> None: 
        self.id: int = id
        self.name: str = ""
        self.priority: int = 0
        self.even_priority: bool = True
        self.owner: Player = Player.EVEN
        self.next: set[Vertex] = set()
        self.prev: set[Vertex] = set()

        # Tuple for small progress measures algo 
        self.tuple: Tuple = None 
        self.stable: bool = False 

    def parse_vertex(self, vertex_info: str, other_vertices: list[Vertex]) -> None: 
        self.priority = int(vertex_info[1])
        self.even_priority = (self.priority % 2) == 0 
        self.owner = Player.EVEN if int(vertex_info[2]) else Player.ODD
        for next_id in vertex_info[3].split(','): 
            self.add_transition(other_vertices[int(next_id)])
        self.name = " ".join(vertex_info[4:]).strip("\"") if len(vertex_info) > 4 else ''
    
    def add_transition(self, other: Vertex) -> None: 
        self.next.add(other)
        other.prev.add(self)
    
    def __str__(self) -> str: 
        return "{id} ({name}): {transitions}".format(id=self.id, name=self.name, transitions=self.next)

    def __repr__(self) -> str:
        return self.name if self.name != '' else str(self.id)
