from __future__ import annotations
import copy 

class Field:
    def __init__(self, init_value:int = None) -> None:
        if init_value is None:
            self.domain = [x for x in range(1,10)]
            self.value = 0
        else:
            self.value = init_value
            self.domain = [init_value]
        
    def get_value(self) -> int:
        return self.value

    def set_value(self, value:int) -> None:
        self.value = value

    #neighbour functions

    def set_neighbours(self, neighbours: list('Field')) -> None:
        self.neighbours = neighbours

    def get_neighbours(self) -> list('Field'):
        return self.neighbours
    
    def get_other_neighbours(self, field: Field) -> list('Field'):
        new_neighbours = self.neighbours.copy()
        new_neighbours.remove(field)
        return new_neighbours

    
    #domain functions

    def get_domain(self) -> list(int):
        return self.domain

    def get_domain_size(self) -> int:
        return len(self.domain)
    
    def remove_from_domain(self, value:int) -> bool:
        before = len(self.domain)

        if value in self.domain:
            self.domain.remove(value)

        if len(self.domain) == 1:
            self.set_value(self.domain[0])

        if len(self.domain) == before:
            return False
        else:
            return True
        
    def __str__(self):
        if self.value == 0:
            return "."
        else:
            return str(self.value)
