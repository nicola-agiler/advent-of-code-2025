from abc import ABC
from functools import cached_property
import re


class Day3(ABC):
    def __init__(self,
                 input_path: str="input.txt"):
        self.input_path: str = input_path

    @cached_property
    def input(self) -> list[str]:
        with open(self.input_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]


class Part1(Day3):

    def regex_to_find_matches(self, number: int) -> str:
        starts_with: str = str(number)[0]
        ends_with: str = str(number)[1]
        return rf"{starts_with}.*?{ends_with}"

    def bank_contains_number(self,
         bank: str,
         number: int) -> bool:
        return re.search(
            pattern=self.regex_to_find_matches(
                number=number),
            string=bank) is not None

    def bank_largest_joltage(self, bank: str):
        for i in range(100, 9, -1):
            if self.bank_contains_number(
                    bank=bank,
                    number=i):
                return i
        return -1

    def solve(self):
        total_output_joltage = 0
        for row in self.input:
            print(self.bank_largest_joltage(bank=row))
            total_output_joltage += self.bank_largest_joltage(
                bank=row
            )
        return total_output_joltage




class Part2(Day3):

    def max_digit_per_string(self,
             string: str,
             upper_bound: int) -> str:
        return str(
            max(
                int(character) for character in string
                if int(character)<upper_bound
            )
        )

    def has_n_more_digits_at_its_right(self,
        bank: str,
        position: int,
        required_digits_at_right: int) -> bool:
        return len(bank[position+1:]) >= required_digits_at_right

    def compute_all_possible_joltages(self,
        bank: str,
        length: int) -> list[str] | None:

        positions_of_max_digit = []
        upper_bound = 10

        if length == 1:
            return [self.max_digit_per_string(
                string=bank,
                upper_bound=upper_bound,)]

        while positions_of_max_digit == []:
            max_digit = self.max_digit_per_string(
                string=bank,
                upper_bound=upper_bound
            )

            positions_of_max_digit = [
                i for i, digit in enumerate(bank)
                if digit==max_digit and
                self.has_n_more_digits_at_its_right(
                    bank=bank,
                    position=i,
                    required_digits_at_right=length-1
                )
            ]
            upper_bound -= 1

        all_suffixes = []

        for position in positions_of_max_digit:
            suffix_solutions = self.compute_all_possible_joltages(
                bank=bank[position+1:],
                length=length-1
            )
            all_suffixes.extend(suffix_solutions)

        results = [max_digit + suffix for suffix in all_suffixes]

        return results

    def solve(self):
        total_output_joltage = 0
        for row in self.input:
            joltages_in_row = self.compute_all_possible_joltages(
                    bank=row,
                    length=12
                )
            print(joltages_in_row)
            max_joltage_in_row = max(
                int(value) for value in joltages_in_row
            )
            total_output_joltage += max_joltage_in_row

        return total_output_joltage

