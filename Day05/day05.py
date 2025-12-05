from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

def get_input(input_path: str) -> list[str]:
    with open(input_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def parse_input(lines: list[str]) -> tuple[
        list[tuple[int,int]],
        list[int]
    ]:
    ranges: list[tuple[int,int]] = []
    numbers: list[int] = []
    for line in lines:
        if "-" in line:
            start, end = line.split("-")
            ranges.append((int(start), int(end)))
        else:
            numbers.append(int(line))

    return ranges, numbers

def fresh_items_from_IDs(ranges: list[tuple[int,int]],
                      items_IDs: list[int]) -> int:
    tot_fresh_items = 0
    for item_ID in items_IDs:
        for start, end in ranges:
            if start <= item_ID <= end:
                tot_fresh_items += 1
                break

    return tot_fresh_items

@dataclass
class ID_range:
    start: int
    end: int

class FreshItems():
    def __init__(self, input_ranges: list[tuple[int,int]]) -> None:
        self.IDs_ranges: list[ID_range] = []
        for start, end in input_ranges:
            self.IDs_ranges.append(ID_range(start, end))

    def tot_fresh_items(self) -> int:
        self.remove_overlaps()
        return sum(
            [range.end - range.start + 1 for range in self.IDs_ranges]
        )

    def remove_overlaps(self) -> None:
        self.IDs_ranges.sort(key=lambda el: el.start)
        while True:
            found_merge = False
            for i in range(len(self.IDs_ranges)-1):
                a = self.IDs_ranges[i]
                b = self.IDs_ranges[i+1]
                if self.are_disjoint_two_ranges(a,b):
                    continue
                logger.debug("Merge found")
                merged_range = self.merge_two_ranges(a,b)
                logger.debug(f"Resulting range: {merged_range.start, merged_range.end}")
                del self.IDs_ranges[i+1]
                del self.IDs_ranges[i]
                self.IDs_ranges.insert(i, merged_range)
                logger.debug(f"Updated IDs: {[ (el.start, el.end) for el in self.IDs_ranges ]}")
                found_merge = True
                break
            if not found_merge:
                break

    def are_disjoint_two_ranges(self,
                                first_range: ID_range,
                                second_range: ID_range
                                ) -> bool:
        return (first_range.end < second_range.start
                or second_range.end < first_range.start)

    def merge_two_ranges(
            self,
            ID_range_a: ID_range,
            ID_range_b: ID_range) -> ID_range:

            return ID_range(
                min(ID_range_a.start, ID_range_b.start),
                max(ID_range_a.end, ID_range_b.end)
            )