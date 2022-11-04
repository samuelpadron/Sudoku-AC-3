from .sudoku import Sudoku
from queue import PriorityQueue
from itertools import count
class Game:
    def __init__(self, sudoku: Sudoku) -> None:
        self.sudoku = sudoku
        
    def show_sudoku(self) -> None:
        print(self.sudoku)



    def revise(self, field_a, field_b) -> None:
        #remove all the values in the domain of field_a that have no matching value in the domain of field_b
        # meaning for a value in field_a there are no values different from that in field_b and therefore remove that value from field_a.
        if len(field_b.get_domain()) == 1:
            field_a.remove_from_domain(field_b.get_value())
            #print("removed:", field_b.get_value(), " remaining:", field_a.get_domain())
            return
        
            

    def solve(self) -> bool:
        """Implementation of AC-3 algorithm

        Returns:
            bool: true if the constraints can be satisfied, else false
        """
        #TODO
        #define all the constraints and domains for each field
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
            #print(field_a.get_domain(), field_b.get_domain())
            size = len(field_a.get_domain())
            self.revise(field_a, field_b)
            if len(field_a.get_domain()) == 0:
                return False
            if size != len(field_a.get_domain()): #HERE USE REMOVE_FROM_DOMAIN FUNCTION INSTEAD
                for neighbour in field_a.get_neighbours():
                    if neighbour != field_b :#and len(neighbour.get_domain()) > 1: #check if this is possible because of python objects bullshit
                        queue.put(((len(neighbour.get_domain()),len(field_a.get_domain()), next(index)), (neighbour, field_a)))
        return True

    def valid_solution(self) -> bool:
        """Checks the validity of a sudoku solution

        Returns:
            bool: true if the sudoku solution is correct
        """
        #TODO
        
        return True

