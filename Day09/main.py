from day09 import *
import time

def main():

    input_path = "input.txt"
    input_file = get_input(input_path)

    grid = Grid(input_file=input_file)

    start = time.perf_counter()
    part_1_result = grid.all_possible_rectangles_areas
    end = time.perf_counter()
    print("Part 1 result: ", part_1_result)
    print(f"Part 1 time: {(end - start):.3f} s")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.WARNING,
        format="%(message)s"
    )

    main()