import os

class Sudoku:
    def __init__(self, filename) -> None:
        self.board = self.read_sudoku(filename)
        
    def read_sudoku(self, filename: str) -> None:
        script_path = os.path.dirname(os.path.abspath(__file__))
        path_list = script_path.split(os.sep)
        text_directory = path_list[0:len(path_list)-1]
        filepath = "/".join(text_directory) + "/" + filename
        print(filepath)
        with open(filepath) as file:
            print(file.read())