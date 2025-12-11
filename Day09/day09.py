from dataclasses import dataclass
from functools import cached_property
from itertools import combinations
from tqdm import tqdm


def get_input(input_path: str) -> list[str]:
    with open(input_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

@dataclass
class Point:
    x: int
    y: int

class Segment:
    def __init__(self,
             x: int,
             y_range: tuple[int, int]) -> None:
        self.x = x
        self.y_start = y_range[0]
        self.y_end = y_range[1]

class Rectangle:
    def __init__(self, edge_1: Point, edge_2: Point):
        self.x1 = min(edge_1.x, edge_2.x)
        self.x2 = max(edge_1.x, edge_2.x)
        self.y1 = min(edge_1.y, edge_2.y)
        self.y2 = max(edge_1.y, edge_2.y)

    @cached_property
    def area(self):
        return (self.x2 - self.x1 + 1) * (self.y2 - self.y1 + 1)

    @cached_property
    def points(self):
        return [Point(x, y)
                for x in range(self.x1, self.x2 + 1)
                for y in range(self.y1, self.y2 + 1)]

class Grid():
    def __init__(self, input_file: list[str]):
        self.input_file = input_file
        self.edges: list[Point] = []
        for line in self.input_file:
            edge_x, edge_y = line.split(",")
            self.edges.append(
                Point(x=int(edge_x), y=int(edge_y)
                      )
            )

    @cached_property
    def largest_possible_rectangles_area(self) -> int:
        rectangles_areas: list[int] = []
        for edge_1, edge_2 in combinations(self.edges, 2):
            rectangles_areas.append(Rectangle(edge_1, edge_2).area)
        return max(rectangles_areas)

    @cached_property
    def vertical_segments(self) -> list[Segment]:
        segments: list[Segment] = []
        pts = self.edges + [self.edges[0]]  # chiude il poligono
        for p1, p2 in zip(pts, pts[1:]):
            if p1.x == p2.x:
                segments.append(
                    Segment(
                        x=p1.x,
                        y_range=(min(p1.y, p2.y), max(p1.y, p2.y))
                    )
                )
        print("Vertical segments:", [(s.x, s.y_start, s.y_end) for s in segments])
        return segments

    @cached_property
    def horizontal_segments(self) -> list[Segment]:
        segments: list[Segment] = []
        pts = self.edges + [self.edges[0]]  # chiude il poligono
        for p1, p2 in zip(pts, pts[1:]):
            if p1.y == p2.y:
                segments.append(
                    Segment(
                        x=p1.y,
                        y_range=(min(p1.x, p2.x), max(p1.x, p2.x))
                    )
                )
        print("Horizontal segments:", [(s.x, s.y_start, s.y_end) for s in segments])
        return segments

    def point_on_perimeter(self, x:int, y: int) -> bool:
        for segment in self.vertical_segments:
            if (x == segment.x and
                segment.y_start <= y <= segment.y_end):
                return True
        for segment in self.horizontal_segments:
            if (y == segment.x and
             segment.y_start <= x <= segment.y_end):
                return True
        return False

    def point_in_area(self, x: int, y: int) -> bool:
        if self.point_on_perimeter(x, y):
            return True

        crossings = 0
        for seg in self.vertical_segments:
            if x < seg.x and seg.y_start<=y<seg.y_end:
                crossings += 1

        return (crossings % 2) == 1

    def rectangle_fully_inside(self, rect: Rectangle) -> bool:

        # Early reject sui vertici
        if (
                not self.point_in_area(rect.x1, rect.y1) or
                not self.point_in_area(rect.x1, rect.y2) or
                not self.point_in_area(rect.x2, rect.y1) or
                not self.point_in_area(rect.x2, rect.y2)
        ):
            return False

        # Controlla lato sinistro e destro
        for y in range(rect.y1, rect.y2 + 1):
            if not self.point_in_area(rect.x1, y): return False
            if not self.point_in_area(rect.x2, y): return False

        # Controlla lato superiore e inferiore
        for x in range(rect.x1, rect.x2 + 1):
            if not self.point_in_area(x, rect.y1): return False
            if not self.point_in_area(x, rect.y2): return False

        return True

    @cached_property
    def largest_area_constrained(self) -> int:
        all_combos = sorted(combinations(self.edges, 2),
                               key=lambda p: Rectangle(*p).area,
                               reverse=True)
        for (e1, e2) in tqdm(all_combos, desc="Rectangles"):
            rect = Rectangle(e1, e2)
            if self.rectangle_fully_inside(rect):
                return rect.area
        return 0
