from day04 import *

def main():

    input_path = "input.txt"
    input_file = get_input(input_path)

    grid = Grid(input_file=input_file)
    result = grid.count_accessible_cells()
    print("Part 1 result:", result)

if __name__ == "__main__":
    main()