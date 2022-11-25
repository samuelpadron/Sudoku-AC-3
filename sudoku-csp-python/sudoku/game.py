from __future__ import annotations
from typing import Optional
from .sudoku import Sudoku
from queue import PriorityQueue
from itertools import count, product, groupby
from operator import itemgetter
from .field import Field


class Game:
    def __init__(self, sudoku: Sudoku) -> None:
        self.__moves__ = 0
        self.sudoku = sudoku
        
    def show_sudoku(self) -> None:
        print(self.sudoku)

    def solve(self, min_values_heuiristic: bool ,max_degree_heuristic: bool) -> bool:
        """summary: try to solve the sudoku by using ac-3 and backtracking

        Args:
            max_degree_heuristic (bool): boolean that says if we want to use the max degree heuristic

        Returns:
            bool: true if we were able to solve, false otherwise
        """
        return self.ac_3() and self.backtrack_search(min_values_heuiristic, max_degree_heuristic)
    
    def revise(self, field_a: Field, field_b: Field) -> bool:
        """summary: revise function used by ac-3, it checks whether it can remove the constraint, which is when field_b
        has a fixed value and therefore field_a can remove that value from his domain.

        Args:
            field_a (Field): field for which we are revising
            field_b (Field): neighbour of field_a for which we check the constraint

        Returns:
            bool: true if value gets removed from domain of field_a, false otherwise
        """
        if len(field_b.get_domain()) == 1:
            return field_a.remove_from_domain(field_b.get_value())
            
        return False
    

    def ac_3(self) -> bool:
        """summary: Implementation of AC-3 algorithm

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


    def backtrack_search(self, min_values_heuiristic: bool, max_degree_heuristic: bool) -> bool:
        """summary: backtrack search algorithm 

        Args:
            min_values_heuristic (bool): boolean meaning if we use the values heuristic
            max_degree_heuristic (bool): boolean meaning if we use the max degree heuristic

        Returns:
            bool: true if backtracking found a solution, false otherwise
        """
        if min_values_heuiristic:
            field = self.find_by_minimum_remaining_values_heuristic(self.sudoku.board, max_degree_heuristic)
        else: 
            field = self.find_by_order_heuristic(self.sudoku.board)


        self.__moves__ += 1
        if field is None:
            return True

        for guess in field.get_domain(): #first use guesses from value heuristic 
            if self.guess_is_valid(guess, field):
                field.set_value(guess)
                if self.backtrack_search(min_values_heuiristic, max_degree_heuristic):
                    return True
            
            field.value = 0
        return False
    
    
    def guess_is_valid(self, guess: int, field: Field) -> bool:
        """summary: check if guess is allowed according to the rules of Sudoku

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

    def find_by_order_heuristic(self, board: Sudoku) -> Optional[Field]:
        """summary: return the first empty Field by index order (so top left first) in the sudoku board

        Args:
            board (Sudoku): the sudoku board for which we are doing backtracking

        Returns:
            Field: first field to be chosen based on this heuristic
        """
        try:
            return self.find_empty_fields(board)[0]
        except:
            return None

    def find_by_minimum_remaining_values_heuristic(self, board: Sudoku, max_degree: bool) ->  Optional[Field]:
        """summary: heuristic that returns the field based on heuristic, if max_degree is true also the max_degree heuristic is applied otherwise 
        only the field are ordered only based on the least number of values they have in the domain. If also max degree is used, they are first ordered by min value
        and then the ones with the same numbner of values in the domain are sorted by max number of constraintsm, whoich is in this case the number orf neighbours that do not have 
        a fixed value yet.

        Args:
            board (Sudoku): the sudoku board for which we are doing backtracking
            max_degree (bool): boolean, tryue if we want to also use max_degree heuristic after min value, false if we don't want to use it
        Returns:
            Field: the field that is chosen based on this heuristic 
        """
        empty_fields = self.find_empty_fields(board)
        if len(empty_fields) == 0:
            return None
        fields  = list(map(lambda y: y[0], [list(group) for _, group in groupby(sorted(map(lambda x: (x, len(x.get_domain())), empty_fields), key=lambda x: x[1]), itemgetter(1))][0]))
        if max_degree:
            fields = [x[0] for x in sorted(map(lambda x: (x, len(list(filter(lambda x: x.get_value() == 0, x.get_neighbours())))), fields), key=lambda x: x[1], reverse=False)]
            
        return fields[0]

    def find_empty_fields(self, board:Sudoku) -> list[Field]:
        """summary: put in a list in order from left to right and from top to bottom the empty fields in the sudoku 
        and return that list

        Args:
            board (Sudoku): the sudoku board gfor which we are doing backtracking

        Returns:
            list[Field]: list of empty fields in the sudoku board
        """
        empty_fields = []
        for row in range(len(board)):
            for col in range(len(board)):
                if board[row][col].value == 0:
                    empty_fields.append(board[row][col])
        return empty_fields

    def list_is_valid(self, listOfElems: list[int]) -> bool:
        """summary: Check if given list contains any duplicates

        Args:
            listOfElems (list[int]): _description_

        Returns:
            bool: true if it does not contain any duplicates, false otherwise
        """
        return len(listOfElems) == len(set(listOfElems))



    def valid_solution(self) -> bool:
        """summary: Checks the validity of a sudoku solution

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
