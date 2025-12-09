from day09 import *

class TestFreshItems:
    def test_part_2(self):
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
        input = [line.strip() for line in input_file if line.strip()]

        test_grid = Grid(input_file=input)

        max_area = test_grid.all_possible_rectangles_areas
        assert(max_area==50)