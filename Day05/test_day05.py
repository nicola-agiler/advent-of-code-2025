from day05 import *
logging.basicConfig(
        level=logging.DEBUG,
        format="%(message)s"
    )
class TestFreshItems:
    def test_part_2(self):
        input_file = """
        3-5
        10-14
        16-20
        12-18
        """.splitlines()
        input = [line.strip() for line in input_file if line.strip()]
        ranges, _ = parse_input(input)

        part2 = FreshItems(input_ranges=ranges)

        assert(part2.tot_fresh_items()==14)
