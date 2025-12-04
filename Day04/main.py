from day04 import *
import time

def main():

    input_path = "input.txt"
    input_file = get_input(input_path)

    # ---------------------
    # PART 1
    # ---------------------
    start = time.perf_counter()
    grid = Grid(input_file=input_file)
    result = grid.count_accessible_rolls_of_paper()
    end = time.perf_counter()

    print("Part 1 result:", result)
    print(f"Part 1 time: {(end - start) * 1000:.3f} ms")

    # ---------------------
    # PART 2
    # ---------------------
    grid = Grid(input_file=input_file)  # nuovo grid: part 2 parte da zero
    start = time.perf_counter()
    print("Part 2 result:")
    grid.remove_rolls_in_cycles()
    end = time.perf_counter()

    print(f"Part 2 time: {(end - start):.3f} s")

if __name__ == "__main__":
    main()