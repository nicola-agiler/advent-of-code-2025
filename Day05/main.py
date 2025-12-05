from day05 import *
import time

def main():

    input_path = "input.txt"
    input_file = get_input(input_path)

    ranges, numbers = parse_input(input_file)

    print("Ranges:", ranges)
    print("Numbers:", numbers)

    result_part_1 = fresh_items_from_IDs(ranges, numbers)
    print("Part 1 result:", result_part_1)

    part2 = FreshItems(input_ranges=ranges)
    result_part_2 = part2.tot_fresh_items()
    print("Part 2 result:", result_part_2)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(message)s"
    )

    main()