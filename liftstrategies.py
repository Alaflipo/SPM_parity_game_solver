from __future__ import annotations

from vertex import Vertex

import random 
from queue import Queue

class LiftStrategy: 

    def __init__(self, vertices: list[Vertex]): 
        self.vertices = vertices
        self.n_vertices = len(vertices)

    def next_vertex(self) -> Vertex: 
        pass 


class InputLiftStrategy(LiftStrategy): 
    
    def __init__(self, vertices: list[Vertex]): 
        super().__init__(vertices)
        self.count = 0 

    def next_vertex(self) -> Vertex: 
        v: Vertex = self.vertices[self.count]
        self.count = (self.count + 1) % self.n_vertices
        return v 
    
class RandomLiftStrategy(LiftStrategy): 
    
    def __init__(self, vertices: list[Vertex]): 
        super().__init__(vertices)
        
        random.seed(1234)
        self.vertices = random.sample(vertices, self.n_vertices)  
        self.count = 0 

    def next_vertex(self) -> Vertex: 
        v: Vertex = self.vertices[self.count]
        self.count = (self.count + 1) % self.n_vertices
        return v 

class BackTrackLiftStrategy(LiftStrategy): 
    
    def __init__(self, vertices: list[Vertex]): 
        super().__init__(vertices)
        self.Q = Queue(maxsize=self.n_vertices)
        for v in self.vertices: 
            self.Q.put(v)

    def next_vertex(self) -> Vertex: 
        v: Vertex = self.vertices[self.count]
        self.count = (self.count + 1) % self.n_vertices
        return v 


