from .sudoku import Sudoku
from queue import PriorityQueue

from itertools import count, chain
from .field import Field
class Game:
    def __init__(self, sudoku: Sudoku) -> None:
        self.sudoku = sudoku
        
    def show_sudoku(self) -> None:
        print(self.sudoku)



    def revise(self, field_a: Field, field_b: Field) -> None:
        taken_values = list(set(list(chain.from_iterable(map(lambda x: x.get_domain(),field_a.get_neighbours())))))
        print(taken_values)
        if len(field_b.get_domain()) == 1:
            field_a.remove_from_domain(field_b.get_value())
            return
        
            

    def solve(self) -> bool:
        """Implementation of AC-3 algorithm

        Returns:
            bool: true if the constraints can be satisfied, else false
        """
        #TODO
        index = count(0)
        fields = self.sudoku.board
        queue = PriorityQueue()
        for i in range(len(fields)):
            for j in range(len(fields[0])):
                field = fields[i][j]
                if len(field.get_domain()) > 1:
                    for neighbour in field.get_neighbours():
                        queue.put(((len(field.get_domain()),len(neighbour.get_domain()), next(index)),(field, neighbour)))
        while not queue.empty():
            ((_,_,_),(field_a, field_b)) = queue.get()
            size = len(field_a.get_domain())
            self.revise(field_a, field_b)
            if len(field_a.get_domain()) == 0:
                return False
            if size != len(field_a.get_domain()): #HERE USE REMOVE_FROM_DOMAIN FUNCTION INSTEAD
                for neighbour in field_a.get_neighbours():
                    if neighbour != field_b and len(neighbour.get_domain()) > 1: #check if this is possible because of python objects bullshit
                        queue.put(((len(neighbour.get_domain()),len(field_a.get_domain()), next(index)), (neighbour, field_a)))
        return True

    def valid_solution(self) -> bool:
        """Checks the validity of a sudoku solution

        Returns:
            bool: true if the sudoku solution is correct
        """
        #TODO
        
        return True

