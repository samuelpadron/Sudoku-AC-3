from .sudoku import Sudoku

class Game:
    def __init__(self, sudoku: Sudoku) -> None:
        self.sudoku = sudoku
        
    def show_sudoku(self) -> None:
        print(self.sudoku)

    def solve(self) -> bool:
        """Implementation of AC-3 algorithm

        Returns:
            bool: true if the constraints can be satisfied, else false
        """
        #TODO
        return True

    def valid_solution(self) -> bool:
        """Checks the validity of a sudoku solution

        Returns:
            bool: true if the sudoku solution is correct
        """
        #TODO
        return True
