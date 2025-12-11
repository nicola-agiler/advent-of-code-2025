from day09 import *

class TestDay9:
    def setup_method(self, method):
        input_file = """
            7,1
            11,1
            11,7
            9,7
            9,5
            2,5
            2,3
            7,3
        """.splitlines()
        self.input = [line.strip() for line in input_file if line.strip()]
        self.test_grid = Grid(input_file=self.input)

    def test_part_1(self):
        max_area = self.test_grid.largest_possible_rectangles_area
        assert max_area == 50

    def test_point_in_area(self):
        assert self.test_grid.point_in_area(3,4)
        assert not self.test_grid.point_in_area(2,1)

    def test_largest_area_constrained(self):
        assert self.test_grid.largest_area_constrained==24