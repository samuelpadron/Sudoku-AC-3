from __future__ import annotations
from .field import Field
import os

class Sudoku:
    def __init__(self, filename) -> None:
        self.board = self.read_sudoku(filename)

    def __str__(self) -> None:
        output = "╔═══════╦═══════╦═══════╗\n"
        for i in range(9):
            if i == 3 or i == 6:
                output += "╠═══════╬═══════╬═══════╣\n"

            output += "║ "

            for j in range(9):
                if j == 3 or j == 6:
                    output += "║ "
                output += str(self.board[i][j]) + " "

            output += "║\n"
        
        output += "╚═══════╩═══════╩═══════╝\n"
        return output

    
        
    def read_sudoku(self, filename: str) -> list[list[Field]]:
        """Read sudoku from file

        Args:
            filename (str): file to open

        Returns:
            list[list[Field]]: 2d list of the sudoku
        """


        grid = [[]]
        assert  filename is not None and filename != "", "invalid filename"
        script_path = os.path.dirname(os.path.abspath(__file__))
        path_list = script_path.split(os.sep)
        text_directory = path_list[0:len(path_list)-1]
        filepath = "/".join(text_directory) + "/" + filename
        grid = []
        try:
            with open(filepath) as file:
                Lines = file.readlines()
        except:
            print(f"error while reading the file: {filename}")
        for line in Lines:
            grid.append(list(map(lambda x : Field() if int(x) == 0 else Field(int(x)) ,list(line.replace("\n","")))))
        self.add_neighbours(grid)
        return grid            

    def add_vertical_neighbours(self, col:int, row:int, grid:list[list[Field]]) -> list[Field]:
        neighbours = [el[col] for el in grid]
        if row < len(grid):
            neighbours = neighbours[0:row] + neighbours[row+1:]    
        else:
            neighbours = neighbours[:-1]
        
        return neighbours

    def add_horizontal_neighbours(self, col:int, row: int, grid:list[list[Field]]):
        neighbours = grid[row]
        if col < len(grid[0]):
            neighbours = neighbours[0:col] + neighbours[col+1:]
        else:
            neighbours = neighbours[:-1]
        
        return neighbours

    def add_square_neighbours(self, col:int, row:int, grid:list[list[Field]]):
        neighbours = []
        square = (int(row/3), int(col/3))
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                next_square = (int(i/3), int(j/3))
                if square == next_square and (row != i or col != j):
                    neighbours.append(grid[i][j])
        return neighbours

      
    def add_neighbours(self, grid: list[list[Field]]) -> None:
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                neighbours = []
                neighbours.extend(self.add_horizontal_neighbours(col, row, grid))
                neighbours.extend(self.add_vertical_neighbours(col, row, grid))
                neighbours.extend(self.add_square_neighbours(col, row, grid))
                grid[row][col].set_neighbours(neighbours)
        