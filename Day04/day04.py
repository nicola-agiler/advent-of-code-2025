from enum import Enum
from collections.abc import Iterator

def get_input(input_path: str) -> list[str]:
    with open(input_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

class CellType(Enum):
    EMPTY = "."
    ROLL = "@"
    REMOVED = "x"

class Grid():
    def __init__(self,
                 input_file: list[str]):
        self.input_file = input_file

        self.columns: int = len(self.input_file[0])
        self.rows: int = len(self.input_file)
        self.padded_grid: list[str] = self.pad_grid()
        self.rows_in_padded_grid: int = len(self.padded_grid)
        self.columns_in_padded_grid: int = len(self.padded_grid[0])
        self.cells: list[list[Cell]] = [
            [Cell(self, row, col)
            for col in range(self.columns_in_padded_grid)]
            for row in range(self.rows_in_padded_grid)
        ]
        self.rolls_of_paper: int = self.count_total_rolls_of_paper()

    # Part 1
    def count_accessible_rolls_of_paper(self) -> int:
        num_accessible_rolls_of_paper: int = 0
        for cell in self.iter_internal_cells():
            if  cell.is_roll_of_paper() and cell.is_accessible_by_forklift():
                num_accessible_rolls_of_paper += 1
        return num_accessible_rolls_of_paper

    def pad_grid(self) -> list[str]:
        padded_grid: list[str] = self.input_file.copy()
        horizontal_pad: str = "." * (self.columns)
        padded_grid.insert(0, horizontal_pad)
        padded_grid.append(horizontal_pad)
        padded_grid = ["." + row + "." for row in padded_grid]

        return padded_grid

    # Part 2
    def remove_rolls_in_cycles(self) -> None:
        cumulative_rolls_removed: int = 0
        while self.rolls_of_paper > 0:
            removed_rolls = self.remove_accessible_rolls_of_paper()
            if removed_rolls == 0:
                break
            self.rolls_of_paper -= removed_rolls
            cumulative_rolls_removed += removed_rolls

            print(f"Removed in cycle: {removed_rolls}; "
                  f"Cumulative removed: {cumulative_rolls_removed}; "
                  f"Remaining: {self.rolls_of_paper} rolls")

    def remove_accessible_rolls_of_paper(self) -> int:
        removed_rolls_of_paper: int = 0
        for cell in self.iter_internal_cells():
            if cell.is_roll_of_paper() and cell.is_accessible_by_forklift():
                self.mark_cell_as_removed(cell)
                removed_rolls_of_paper += 1
        return removed_rolls_of_paper

    def mark_cell_as_removed(self, cell: "Cell") -> None:
        cell.set_type(CellType.REMOVED)

    def count_total_rolls_of_paper(self) -> int:
        tot_rolls_of_paper: int = 0
        for cell in self.iter_internal_cells():
            if cell.is_roll_of_paper():
                tot_rolls_of_paper += 1
        return tot_rolls_of_paper

    def get_cell(self, row: int, column: int) -> "Cell":
        return self.cells[row][column]

    def iter_internal_cells(self) -> Iterator["Cell"]:
        for row in range(1, self.rows_in_padded_grid):
            for column in range(1, self.columns_in_padded_grid):
                yield self.cells[row][column]

class Cell():
    def __init__(self,
                 grid: Grid,
                 row: int,
                 column: int,):
        self.grid = grid
        self.row = row
        self.column = column
        char: str = self.grid.padded_grid[self.row][self.column]
        self.type = CellType(char)

    def set_type(self, new_type: str) -> None:
        self.type = new_type

    def adjacent_cells(self) -> list["Cell"]:
        left = self.grid.get_cell(self.row, self.column - 1)
        right = self.grid.get_cell(self.row, self.column + 1)
        up = self.grid.get_cell(self.row - 1, self.column)
        down = self.grid.get_cell(self.row + 1, self.column)
        upright = self.grid.get_cell(self.row - 1, self.column + 1)
        upleft = self.grid.get_cell(self.row - 1, self.column - 1)
        downright = self.grid.get_cell(self.row + 1, self.column + 1)
        downleft = self.grid.get_cell(self.row + 1, self.column - 1)
        return [left, right, up, down, upright, upleft, downright, downleft]

    def is_roll_of_paper(self) -> bool:
        return self.type == CellType.ROLL

    def rolls_of_paper_in_adjacent_cells(self) -> int:
        num_rolls = 0
        for cell in self.adjacent_cells():
            if cell.is_roll_of_paper():
                num_rolls += 1
        return num_rolls

    def is_accessible_by_forklift(self) -> bool:
        return self.rolls_of_paper_in_adjacent_cells() < 4




