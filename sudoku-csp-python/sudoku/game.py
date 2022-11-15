from __future__ import annotations
from .sudoku import Sudoku
from queue import PriorityQueue
from itertools import count, chain, product
from .field import Field

class Game:
    def __init__(self, sudoku: Sudoku) -> None:
        self.__moves__ = 0
        self.sudoku = sudoku
        
    def show_sudoku(self) -> None:
        print(self.sudoku)

    def solve(self) -> bool:
        return self.ac_3() and self.backtrack_search()
    
    def revise(self, field_a: Field, field_b: Field) -> bool:
        #neighbour1, neighbour2, neighbour3 = field_a.get_neighbours()[0:8], field_a.get_neighbours()[8:16], field_a.get_neighbours()[16:24]
        #for neighbours in [neighbour1, neighbour2, neighbour3]:
        #    taken_values = list(set(list(chain.from_iterable(map(lambda x: x.get_domain(),neighbours)))))
#
        #    if len(taken_values) == 8:
        #        res = [value for value in range(1,10) if value not in taken_values] #get missing value in a list
        #        field_a.set_domain(res)
        #        field_a.set_value(res[0])
        #        return True

        if len(field_b.get_domain()) == 1:
            return field_a.remove_from_domain(field_b.get_value())
            
        return False
    

    def ac_3(self) -> bool:
        """Implementation of AC-3 algorithm

        Returns:
            bool: true if the constraints can be satisfied, else false
        """
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
            if len(field_a.get_domain()) > 1 and self.revise(field_a, field_b):
                for neighbour in field_a.get_neighbours():
                    if neighbour != field_b and len(neighbour.get_domain()) > 1: #check if this is possible because of python objects bullshit
                        queue.put(((len(neighbour.get_domain()),len(field_a.get_domain()), next(index)), (neighbour, field_a)))
        return True


    def backtrack_search(self) -> bool:
        field = self.find_empty_field(self.sudoku.board) #no heuristic
        #field = self.find_by_minimum_remaining_values_heuristic(self.sudoku.board) #heuristic for empty field to be done
        #field = self.find_by_max_degree_heuristuc(self.sudoku.board)
        self.__moves__ += 1
        if field is None:
            return True

        for guess in field.get_domain(): #first use guesses from value heuristic 
            if self.guess_is_valid(guess, field):
                field.set_value(guess)
                if self.backtrack_search():
                    return True
            
            field.value = 0
        return False
    
    
    def guess_is_valid(self, guess: int, field: Field) -> bool:
        """check if guess is allowed according to the rules of Sudoku

        Args:
            guess (_type_): value being guessed
            row (_type_): row of the field where the guess is being placed
            col (_type_): column of the field where the guess being placed

        Returns:
            bool: guess is valid
        """
        neighbours = list(map(lambda x: x.get_value(), field.get_neighbours()))
        if guess in neighbours:
            return False
        return True

    def find_by_max_degree_heuristuc(self, board: Sudoku) -> Field:
        empty_fields = self.find_empty_fields(board)
        if len(empty_fields) == 0:
            return None
        return sorted(map(lambda x: (x, len(list(filter(lambda x: x.get_value() == 0, x.get_neighbours())))), empty_fields), key=lambda x: x[1])[-1][0]

    def find_by_minimum_remaining_values_heuristic(self, board: Sudoku) -> Field:
        empty_fields = self.find_empty_fields(board)
        if len(empty_fields) == 0:
            return None
        return sorted(map(lambda x: (x, len(x.get_domain())), empty_fields), key=lambda x: x[1])[0][0]

    def find_empty_fields(self, board:Sudoku) -> list[Field]:
        empty_fields = []
        for row in range(len(board)):
            for col in range(len(board)):
                if board[row][col].value == 0:
                    empty_fields.append(board[row][col])
        return empty_fields

    def find_empty_field(self, board: Sudoku) -> Field:
        """Find next field in the Sudoku that has no value assigned yet

        Args:
            board (Sudoku): the board to check

        Returns:
            tuple[int, int]: the coordinates of the field
        """
        for row in range(len(board)):
            for col in range(len(board)):
                if board[row][col].value == 0:
                    return board[row][col]
        
        return None


    def list_is_valid(self, listOfElems) -> bool:
        ''' Check if given list contains any duplicates '''
        if len(listOfElems) == len(set(listOfElems)):
            return True
        else:
            return False


    def valid_solution(self) -> bool:
        """Checks the validity of a sudoku solution

        Returns:
            bool: true if the sudoku solution is correct
        """

        b = True
        board = self.sudoku.board
        
        for row, col in product(range(len(board)), range(len(board[0]))):
            b = self.list_is_valid(list(map(lambda x: x.get_value() ,[el[col] for el in board])))
            if not b:
                return False
            b = self.list_is_valid(list(map(lambda x: x.get_value(), board[col])))
            if not b:
                return False
            if col in [0,3,6] and row in [0,3,6]:
                l = list(map(lambda x: x.get_value(), board[row][col].get_neighbours()[16:24]))
                l.append(board[row][col].get_value())
                b = self.list_is_valid(l)
                if not b:
                    return False
        return True