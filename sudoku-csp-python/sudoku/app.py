from __future__ import annotations
from .game import Game
from .sudoku import Sudoku

class App:
    def __init__(self) -> None:
        #filepath = input("Enter a sudoku text file\n")
        self.start("Sudoku1.txt")

    def start(self, filepath: str) -> None:
        game1 = Game(Sudoku(filepath))
        game1.show_sudoku()
        if game1.solve() and game1.valid_solution():
            print("Solved!")
        else:
            print("Could not solve this sudoku D:")
        game1.show_sudoku()

