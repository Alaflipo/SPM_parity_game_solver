from __future__ import annotations

from vertex import Vertex, Player

import random 
from queue import Queue

class LiftStrategy: 

    def __init__(self, vertices: list[Vertex]): 
        self.vertices = vertices
        self.n_vertices = len(vertices)

    def next_vertex(self) -> Vertex: 
        pass 

    def was_lifted(self, v: Vertex) -> None: 
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
        self.Q: Queue[Vertex] = Queue(maxsize=self.n_vertices)
        self.in_queue: list[bool] = [True for i in range(self.n_vertices)] 
        for v in self.vertices: 
            self.Q.put(v)

    def next_vertex(self) -> Vertex: 
        if (self.Q.empty()): 
            print("Queue is empty!!!")
            return None
        else: 
            v: Vertex = self.Q.get()
            self.in_queue[v.id] = False
            return v 
        
    def was_lifted(self, v: Vertex): 
        for w in v.prev: 
            if (not self.in_queue[w.id] and not w.tuple.top): 
                self.in_queue[w.id] = True 
                self.Q.put(w)

class SelfLoopStrategy(LiftStrategy): 

    def __init__(self, vertices: list[Vertex]): 
        super().__init__(vertices)
        self.count = 0 
        self.split_value = 0 # used to determine where self-loops stop 

        # split the vertices in ones that have a self-loop and ones that don't 
        odd_self_loop: list[Vertex] = []
        no_odd_self_loop: list[Vertex] = [] 
        for v in self.vertices: 
            found_loop = False 
            if (v.owner == Player.ODD and not v.even_priority): 
                for next_v in v.next: 
                    if (v.id == next_v.id): 
                        # if we found an odd self loop
                        odd_self_loop.append(v)
                        self.split_value += 1 
                        found_loop = True 
                        break 
            # if we have not found an odd self loop
            if (not found_loop): 
                no_odd_self_loop.append(v)
        # input order with odd self loops first 
        self.vertices = odd_self_loop + no_odd_self_loop

    def next_vertex(self) -> Vertex: 
        v: Vertex = self.vertices[self.count]
        if (self.count <= self.split_value): 
            # When we have reached the top with a self-loop vertex we continue with the next
            if (v.tuple.top): 
                v.stable = True
                self.count = (self.count + 1) % len(self.vertices)
                return self.next_vertex()
        else: 
            self.count = (self.count + 1) % len(self.vertices)
        return v 




