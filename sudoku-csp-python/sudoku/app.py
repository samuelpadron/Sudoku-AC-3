from __future__ import annotations
from .game import Game
from .sudoku import Sudoku
import matplotlib.pyplot as plt



class App:
    def __init__(self) -> None:
        #filepath = input("Enter a sudoku text file\n")
        self.counts = []
        self.min_values_heuristic = True
        for max_degree_heuristic in [False, True]:
            for n in range(1,6):
                self.max_degree_heuirstic = max_degree_heuristic
                self.start(f"Sudoku{n}.txt")
        self.min_values_heuristic = False
        for n in range(1,6):
            self.start(f"Sudoku{n}.txt")
        l = [0,1,2,3,4]
        h1, h2, h3 = self.counts[0:5], self.counts[5:10], self.counts[10:15]
        print(h1,h2,h3)
 


    def start(self, filepath: str) -> None:
        game1 = Game(Sudoku(filepath))
        game1.show_sudoku()
        
        if game1.solve(self.min_values_heuristic, self.max_degree_heuirstic) and game1.valid_solution():
            moves = game1.__moves__
            self.counts.append(moves)
            print(f"Solved in {moves} moves!")
        else:
            print("Could not solve this sudoku D:")
        game1.show_sudoku()
        