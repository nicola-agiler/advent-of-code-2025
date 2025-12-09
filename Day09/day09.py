from dataclasses import dataclass
import logging
from functools import cached_property
from itertools import combinations

logger = logging.getLogger(__name__)

def get_input(input_path: str) -> list[str]:
    with open(input_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

@dataclass
class Edge:
    x: int
    y: int

class Rectangle:
    def __init__(self,
        edge_1: Edge,
        edge_2: Edge
        ):
        self.edge_1 = edge_1
        self.edge_2 = edge_2

    def area(self) -> int:
        return (
            abs(self.edge_1.x - self.edge_2.x + 1)
            *
            abs(self.edge_1.y - self.edge_2.y + 1)
        )

class Grid():
    def __init__(self, input_file: list[str]):
        self.input_file = input_file
        self.edges: list[Edge] = []
        for line in self.input_file:
            edge_x, edge_y = line.split(",")
            self.edges.append(
                Edge(
                    x=int(edge_x),
                    y=int(edge_y)
                )
            )

    @cached_property
    def all_possible_rectangles_areas(self) -> list[int]:
        rectangles = []
        for edge_1, edge_2 in combinations(self.edges, 2):
            rectangles.append(Rectangle(edge_1, edge_2).area())
        return max(rectangles)
