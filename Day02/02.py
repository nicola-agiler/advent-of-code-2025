from abc import ABC
from functools import cached_property
from itertools import chain

class Day1(ABC):
    def __init__(self,
                 input_path: str="input.txt"):
        self.input_path: str = input_path

    def read_input(self) -> list[tuple[int, int]]:
        with open(self.input_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        ranges: list[tuple[int, int]] = []
        for part in content.split(","):
            if not part.strip():  # ignora pezzi vuoti
                continue
            start, end = part.split("-")
            ranges.append((int(start), int(end)))

        return ranges

class Part1(Day1):

    def digits_in_number(self, number: int) -> int:
        return len(str(number))

    def max_num_of_digits(self) -> int:
        ranges = self.read_input()
        return max(
            [self.digits_in_number(range_end) for _, range_end in ranges]
        )

    def max_possible_period(self):
        return self.max_num_of_digits() // 2

    def generate_repetitions(self, length: int, num_of_periods: list=[]) -> list[int]:

        if len(num_of_periods) == 0:
            num_of_periods = [2]

        repetitions = []

        for period in num_of_periods:
            if length%period == 0:
                period_length = length//period

                for number in range(10 ** (period_length-1), 10 ** period_length):
                    repetition_str: str = str(number)
                    repeated_number = int(
                        repetition_str * period
                    )
                    repetitions.append(repeated_number)

        return repetitions

    @cached_property
    def generate_all_possible_repetitions(self) -> list[int]:

        max_length = self.max_num_of_digits()
        all_possible_repetitions = []
        for num_of_digits in range(2, max_length + 1):
            all_possible_repetitions.append(
                self.generate_repetitions(num_of_digits)
            )

        return list(set([x for y in all_possible_repetitions for x in y]))

    def invalid_ids_in_range(self,
                 start: int,
                 end: int)-> list[int]:
        return [id for id in
                self.generate_all_possible_repetitions
                if start <= id <= end
                ]

    def all_invalid_ids(self) -> list[int]:
        all_invalid_ids = []
        for start, end in self.read_input():
            all_invalid_ids.append(
                self.invalid_ids_in_range(start, end)
            )
        return all_invalid_ids

    def solve(self):
        return sum(
            [id for range in self.all_invalid_ids()
        for id in range])

class Part2(Part1):
    @cached_property
    def generate_all_possible_repetitions(self) -> list[int]:
        max_length = self.max_num_of_digits()
        all_possible_repetitions = []
        for num_of_digits in range(2, max_length + 1):
            periods_list = [num_of_digits//i for i in range(1, num_of_digits//2+1) if num_of_digits%i==0]
            all_possible_repetitions.append(
                self.generate_repetitions(length=num_of_digits, num_of_periods=periods_list)
            )

        return list(set([x for y in all_possible_repetitions for x in y]))

def main():

    part1 = Part1()
    print(part1.read_input()[:5])
    print("Generate repetitions:", part1.generate_repetitions(length=2))
    print("All possible repetitions:",
          part1.generate_all_possible_repetitions[-100:]
    )
    print("Invalid ids test:", part1.invalid_ids_in_range(start=95, end=115))
    print("All invalid ids:", part1.all_invalid_ids()[-100:])
    print(626262 in part1.generate_all_possible_repetitions)
    print("Solution:", part1.solve())

    print("#"*30)
    print("Part 2")
    part2 = Part2()
    print("Invalid ids test:", part2.invalid_ids_in_range(start=1698522, end=1698528))
    print("All invalid ids:", sorted(part2.generate_all_possible_repetitions[:200]))
    print(626262 in part2.generate_all_possible_repetitions)
    print("Invalid ids in input file:", sorted(part2.all_invalid_ids()))
    print("Solution:", part2.solve())



if __name__ == "__main__":
    main()