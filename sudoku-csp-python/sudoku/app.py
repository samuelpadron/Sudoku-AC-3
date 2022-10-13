from mimetypes import init
from .game import Game
from .sudoku import Sudoku

class App:
    def __init__(self) -> None:
        filepath = input("Enter a sudoku text file")
        print(filepath)
        self.start(filepath)

    def start(self, filepath: str) -> None:
        game1 = Game(Sudoku(filepath))
        game1.show_sudoku()

