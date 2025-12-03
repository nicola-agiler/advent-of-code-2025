from abc import ABC
import pandas as pd


class Day1(ABC):
    def __init__(self,
                 input_path: str="input/input.txt"):
        self.input_path: str = input_path

    def read_input(self) -> list[str]:
        with open(self.input_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    def input_to_array(self) -> list[int]:
        """
        Converte righe tipo 'R11', 'L47' in interi:
        - 'R' → numero positivo
        - 'L' → numero negativo
        Il valore è la parte dopo il primo carattere.
        """
        numeri = []
        rows = self.read_input()
        for r in rows:
            direzione = r[0]
            valore = int(r[1:])
            if direzione == "L":
                numeri.append(-valore)
            elif direzione == "R":
                numeri.append(valore)
            else:
                raise ValueError(f"Direzione sconosciuta: {direzione}")
        return numeri


class Part1(Day1):

    def passages_at_zero(self,
                         values: list[int]):
        passages_at_zero: int = 0
        running_sum: int = 0

        for value in values:
            running_sum += value
            if running_sum % 100 == 50:
                passages_at_zero += 1

        return passages_at_zero

    def solve(self):
        input: list[str] = self.read_input()
        numeri: list[int] = self.input_to_array()
        passages_at_zero: int = self.passages_at_zero(numeri)
        return passages_at_zero

class Part2(Day1):

    STARTING_POSITION = 50

    def final_position(self, current_position: int,
                              rotation: int) -> int:
        return (current_position + rotation) % 100

    def anti_clockwise_distance_from_zero(self, current_position: int) -> int:
        return current_position

    def clockwise_distance_from_zero(self, current_position: int) -> int:
        return (100-current_position)%100

    def rotation_passes_over_zero(self,
                            current_position: int,
                            rotation: int) -> int:
        passes_over_zero: int = 0

        if rotation < 0:
            # anti-clockwise
            remaining_rotation_after_first_pass_to_zero: int = (
                    abs(rotation) -
                    self.anti_clockwise_distance_from_zero(current_position)
            )
        else:
            # clockwise
            remaining_rotation_after_first_pass_to_zero: int = (
                    rotation -
                    self.clockwise_distance_from_zero(current_position)
            )

        if remaining_rotation_after_first_pass_to_zero >= 0:
            if not current_position == 0:
                passes_over_zero += 1
            remaining_passes_over_zero: int = remaining_rotation_after_first_pass_to_zero//100
            passes_over_zero += remaining_passes_over_zero

        return passes_over_zero

    def total_passes_over_zero(self,):

        log = {
            "step": [],
            "start_pos": [],
            "rotation": [],
            "end_pos": [],
            "passes": [],
            "passes_cumulative": [],
        }

        total_passes_over_zero: int = 0
        last_position = self.STARTING_POSITION
        rotations: list[int] = self.input_to_array()

        for i, rotation in enumerate(rotations, start=1):
            total_passes_over_zero += self.rotation_passes_over_zero(
                current_position=last_position,
                rotation=rotation
            )

            # log
            log["step"].append(i)
            log["start_pos"].append(last_position)
            log["rotation"].append(rotation)
            log["end_pos"].append(self.final_position(
                current_position=last_position,
                rotation=rotation
            ))
            log["passes"].append(self.rotation_passes_over_zero(
                current_position=last_position,
                rotation=rotation
            ))
            log["passes_cumulative"].append(total_passes_over_zero)

            last_position = self.final_position(
                current_position=last_position,
                rotation=rotation
            )
        df = pd.DataFrame(log)
        df.to_csv("debug_steps_part2.csv", index=False)

        return total_passes_over_zero

    def solve(self):
        return self.total_passes_over_zero()


def main():

    part1 = Part1()
    print(part1.input_to_array())

    part1_result = part1.solve()
    print("Part 1:", part1_result)

    part2 = Part2()
    part2_result = part2.solve()
    print("Part 2:", part2_result)


if __name__ == "__main__":
    main()