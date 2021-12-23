import unittest
from day23 import AmphiState, AmphiState2, EMPTY_HALLWAY, space_above_room, run_part_1, run_part_2


class TestSpaceAboveRoom(unittest.TestCase):

    def test_space_above_room(self):
        for room, expected_result in [(0, 2), (1, 4), (2, 6), (3, 8)]:
            result = space_above_room(room)
            self.assertEqual(expected_result, result)


class TestPossibleNextSteps(unittest.TestCase):

    def run_steps_test(self, hallway0, rooms0, hallway1, rooms1, cost):
        first_state = AmphiState(hallway0, rooms0)
        next_step = AmphiState(hallway1, rooms1)
        result = first_state.possible_next_states()
        self.assertIn((next_step, cost), result)

    def test_first_sample_step(self):
        self.run_steps_test(
            EMPTY_HALLWAY, ["BA", "CD", "BC", "DA"],
            "...B.......", ["BA", "CD", ".C", "DA"], 40
        )

    def test_second_sample_step(self):
        self.run_steps_test(
            "...B.......", ["BA", "CD", ".C", "DA"],
            "...B.......", ["BA", ".D", "CC", "DA"], 400
        )

    def test_third_sample_step_part_1(self):
        self.run_steps_test(
            "...B.......", ["BA", ".D", "CC", "DA"],
            "...B.......", ["BA", "D.", "CC", "DA"], 1000
        )

    def test_third_sample_step_part_2(self):
        self.run_steps_test(
            "...B.......", ["BA", "D.", "CC", "DA"],
            "...B.D.....", ["BA", "..", "CC", "DA"], 2000
        )

    def test_third_sample_step_part_3(self):
        self.run_steps_test(
            "...B.D.....", ["BA", "..", "CC", "DA"],
            ".....D.....", ["BA", "B.", "CC", "DA"], 20
        )

    def test_third_sample_step_part_4(self):
        self.run_steps_test(
            ".....D.....", ["BA", "B.", "CC", "DA"],
            ".....D.....", ["BA", ".B", "CC", "DA"], 10
        )

    def test_fourth_sample_step(self):
        self.run_steps_test(
            ".....D.....", ["BA", ".B", "CC", "DA"],
            ".....D.....", [".A", "BB", "CC", "DA"], 40
        )

    def test_fifth_sample_step_part1(self):
        self.run_steps_test(
            ".....D.....", [".A", "BB", "CC", "DA"],
            ".....D.D...", [".A", "BB", "CC", ".A"], 2000
        )

    def test_fifth_sample_step_part2(self):
        self.run_steps_test(
            ".....D.D...", [".A", "BB", "CC", ".A"],
            ".....D.D...", [".A", "BB", "CC", "A."], 1
        )

    def test_fifth_sample_step_part3(self):
        self.run_steps_test(
            ".....D.D...", [".A", "BB", "CC", "A."],
            ".....D.D.A.", [".A", "BB", "CC", ".."], 2
        )

    def test_fifth_sample_step_part4(self):
        self.run_steps_test(
            ".....D.D.A.", [".A", "BB", "CC", ".."],
            ".....D...A.", [".A", "BB", "CC", "D."], 2000
        )

    def test_fifth_sample_step_part5(self):
        self.run_steps_test(
            ".....D...A.", [".A", "BB", "CC", "D."],
            ".....D...A.", [".A", "BB", "CC", ".D"], 1000
        )

    def test_fifth_sample_step_part6(self):
        self.run_steps_test(
            ".....D...A.", [".A", "BB", "CC", ".D"],
            ".........A.", [".A", "BB", "CC", "DD"], 4000
        )

    def test_sixth_sample_step(self):
        self.run_steps_test(
            ".........A.", [".A", "BB", "CC", "DD"],
            "...........", ["AA", "BB", "CC", "DD"], 8
        )

class TestPossibleNextStepsPartTwo(unittest.TestCase):

    def run_steps_test(self, hallway0, rooms0, hallway1, rooms1, cost):
        first_state = AmphiState2(hallway0, rooms0)
        next_step = AmphiState2(hallway1, rooms1)
        result = first_state.possible_next_states()
        self.assertIn((next_step, cost), result)

    def test_first_sample_step(self):
        self.run_steps_test(
            EMPTY_HALLWAY, ["BDDA", "CCBD", "BBAC", "DACA"],
            "..........D", ["BDDA", "CCBD", "BBAC", ".ACA"], 3000
        )

    def test_second_sample_step_part1(self):
        self.run_steps_test(
            "..........D", ["BDDA", "CCBD", "BBAC", ".ACA"],
            "..........D", ["BDDA", "CCBD", "BBAC", "A.CA"], 1
        )

    def test_second_sample_step_part2(self):
        self.run_steps_test(
            "..........D", ["BDDA", "CCBD", "BBAC", "ACA."],
            "A.........D", ["BDDA", "CCBD", "BBAC", ".CA."], 9
        )

    def test_second_sample_step_part3(self):
        self.run_steps_test(
            "A.........D", ["BDDA", "CCBD", "BBAC", ".CA."],
            "A.........D", ["BDDA", "CCBD", "BBAC", "C.A."], 100
        )

    def test_second_sample_step_part4(self):
        self.run_steps_test(
            "A.........D", ["BDDA", "CCBD", "BBAC", "C.A."],
            "A.........D", ["BDDA", "CCBD", "BBAC", "CA.."], 1
        )

    def test_third_sample_step(self):
        self.run_steps_test(
            "A.........D", ["BDDA", "CCBD", "BBAC", "CA.."],
            "A........BD", ["BDDA", "CCBD", ".BAC", "CA.."], 40
        )

    def test_third_sample_step_part2(self):
        self.run_steps_test(
            "A........BD", ["BDDA", "CCBD", ".BAC", "CA.."],
            "A........BD", ["BDDA", "CCBD", "B.AC", "CA.."], 10
        )

    def test_fourth_sample_step(self):
        self.run_steps_test(
            "A........BD", ["BDDA", "CCBD", "BA.C", "CA.."],
            "A......B.BD", ["BDDA", "CCBD", ".A.C", "CA.."], 20
        )

    def test_fifth_sample_step(self):
        self.run_steps_test(
            "A......B.BD", ["BDDA", "CCBD", "A..C", "CA.."],
            "AA.....B.BD", ["BDDA", "CCBD", "...C", "CA.."], 6
        )

    def test_sixth_sample_step(self):
        self.run_steps_test(
            "AA.....B.BD", ["BDDA", "CCBD", "...C", "CA.."],
            "AA.....B.BD", ["BDDA", ".CBD", "C..C", "CA.."], 400
        )

    def test_seventh_sample_step(self):
        self.run_steps_test(
            "AA.....B.BD", ["BDDA", "CBD.", "..CC", "CA.."],
            "AA.....B.BD", ["BDDA", ".BD.", "C.CC", "CA.."], 400
        )

    def test_problematic_step(self):
        self.run_steps_test(
            "AA.....B.BD", ["BDDA", "CB.D", "..CC", "CA.."],
            "AA.....B.BD", ["BDDA", "CBD.", "..CC", "CA.."], 1000
        )



class TestParts(unittest.TestCase):

    def test_example_part_1(self):
        rooms = ["BA", "CD", "BC", "DA"]
        result = run_part_1(rooms)
        self.assertEqual(12521, result)

    def test_example_part_2(self):
        rooms = ["BDDA", "CCBD", "BBAC", "DACA"]
        result = run_part_2(rooms)
        self.assertEqual(44169, result)


if __name__ == '__main__':
    unittest.main()
