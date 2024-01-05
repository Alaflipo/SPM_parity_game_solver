from __future__ import annotations

class Tuple: 
    tuple_size: int = 0
    empty_tuple_values: list[int] = [] 
    max_tuple_values: list[int] = []

    def __init__(self, values): 
        self.values: list[int] = values
        self.top: bool = False
    
    @staticmethod
    def set_tuple_size(value) -> None: 
        Tuple.tuple_size = value 
        Tuple.empty_tuple_values = [0 for _ in range(Tuple.tuple_size)]
    
    @staticmethod
    def set_max_tuple(priorities: list[int]) -> None: 
        Tuple.max_tuple_values = Tuple.empty_tuple_values.copy()
        for p in priorities: 
            if (p % 2 == 1): 
                Tuple.max_tuple_values[p] += 1
    
    @staticmethod
    def get_empty_tuple() -> Tuple: 
        return Tuple(Tuple.empty_tuple_values.copy())
    
    def get(self, index: int) -> int: 
        return self.values[index]
    
    def get_range(self, start: int, end: int) -> list[int]: 
        return self.values[start: end]

    def set_value(self, index: int, value: int) -> None: 
        assert index > -1 and index < len(self.values)
        self.values[index] = value 
    
    def set_value_range(self, start: int, end: int, new_values: list[int]) -> None: 
        assert start > -1 and end <= len(self.values)
        assert (end - start) == len(new_values)
        self.values[start: end] = new_values
    
    def set_top(self, top: bool) -> None: 
        self.top = top 
    
    def add(self, start: int) -> None: 
        index = start 
        while index > 1 and self.values[index] + 1 > Tuple.max_tuple_values[index]: 
            self.values[index] = 0 
            index -= 2

        if self.values[index] + 1 > Tuple.max_tuple_values[index]: 
            self.top = True 
            return 
        self.values[index] += 1
    
    def check_top(self) -> None:
        for i, value in enumerate(self.values): 
            if value > Tuple.max_tuple_values[i]: 
                self.top = True 

    # equality function 
    def __eq__(self, other: Tuple) -> bool:
        if (self.top != other.top): return False 
        if (self.top and other.top): return True 
        for i in range(len(self.values)): 
            # only check the odd values 
            if ((i % 2 == 1) and self.values[i] != other.values[i]): 
                return False 
        return True 
    
    # less then function 
    def __lt__(self, other: Tuple) -> bool: 
        if (self.top): return False 
        if (other.top and not self.top): return True 
        for i in range(len(self.values)): 
            # only check the odd values 
            if (i % 2 == 1): 
                if (self.values[i] < other.values[i]): 
                    return True 
                if (self.values[i] > other.values[i]): 
                    return False 
        return False 
    
    # greater then function 
    def __gt__(self, other: Tuple) -> bool:  
        if (other.top): return False 
        if (self.top and not other.top): return True 
        for i in range(len(self.values)): 
            # only check the odd values 
            if (i % 2 == 1): 
                if (self.values[i] > other.values[i]): 
                    return True 
                if (self.values[i] < other.values[i]): 
                    return False 
        return False 
    
    # less then or equal function 
    def __le__(self, other: Tuple) -> bool: 
        if (self.top): return False 
        if (other.top and not self.top): return True 
        for i in range(len(self.values)): 
            # only check the odd values 
            if (i % 2 == 1): 
                if (self.values[i] < other.values[i]): 
                    return True 
                if (self.values[i] > other.values[i]): 
                    return False 
        return True 
    
    # greater then or equal function 
    def __ge__(self, other: Tuple) -> bool:  
        if (other.top): return False 
        if (self.top and not other.top): return True 
        for i in range(len(self.values)): 
            # only check the odd values 
            if (i % 2 == 1): 
                if (self.values[i] > other.values[i]): 
                    return True 
                if (self.values[i] < other.values[i]): 
                    return False 
        return True 

    def __str__(self) -> str:
        return '{values} ({top})'.format(values=self.values, top=('T' if self.top else ''))
