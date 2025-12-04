from abc import ABC
from functools import cached_property

def get_input(input_path: str) -> list[str]:
    with open(input_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

class Grid():
    def __init__(self,
                 input_file: list[str]):
        self.input_file = input_file
        self.columns = len(self.input_file[0])
        self.rows = len(self.input_file)


    @cached_property
    def padded_grid(self) -> list[str]:
        padded_grid: list[str] = self.input_file.copy()
        horizontal_pad: str = "." * (self.columns)
        padded_grid.insert(0, horizontal_pad)
        padded_grid.append(horizontal_pad)
        padded_grid = ["." + row + "." for row in padded_grid]

        return padded_grid

    def count_accessible_cells(self) -> int:
        num_accessible_cells: int = 0
        for row in range(1, len(self.padded_grid)):
            for col in range(1, len(self.padded_grid[0])):
                cell = Cell(self.padded_grid, row, col)
                if cell.is_accessible_by_forklift():
                    num_accessible_cells += 1

        return num_accessible_cells


class Cell():
    def __init__(self,
                 grid: list[str],
                 x: int,
                 y: int,):
        self.grid = grid
        self.row_coordinate = x
        self.column_coordinate = y

    @cached_property
    def adjacent_cells(self) -> list["Cell"]:
        left = Cell(self.grid, self.row_coordinate, self.column_coordinate-1)
        right = Cell(self.grid, self.row_coordinate, self.column_coordinate+1)
        up = Cell(self.grid,self.row_coordinate-1,self.column_coordinate)
        down = Cell(self.grid, self.row_coordinate+1, self.column_coordinate)
        upright = Cell(self.grid, self.row_coordinate-1, self.column_coordinate+1)
        upleft = Cell(self.grid, self.row_coordinate-1, self.column_coordinate-1)
        downright = Cell(self.grid, self.row_coordinate+1, self.column_coordinate+1)
        downleft = Cell(self.grid, self.row_coordinate+1, self.column_coordinate-1)
        return [left, right, up, down, upright, upleft, downright, downleft]

    @cached_property
    def is_roll_of_paper(self) -> bool:
        return self.grid[self.row_coordinate][self.column_coordinate] == "@"

    @cached_property
    def rolls_of_paper_in_adjacent_cells(self) -> int:
        num_rolls = 0
        for cell in self.adjacent_cells:
            if cell.is_roll_of_paper:
                num_rolls += 1
        return num_rolls

    def is_accessible_by_forklift(self) -> bool:
        if self.is_roll_of_paper and self.rolls_of_paper_in_adjacent_cells < 4:
            return True
        return False




