import unittest
from day18 import *


class TestExplode(unittest.TestCase):

    def run_explode_test(self, input, expected_result):
        result = try_explode(input)
        self.assertEqual(expected_result, result)

    def test_one(self):
        self.run_explode_test(
            [[[[[9, 8], 1], 2], 3], 4],
            [[[[0, 9], 2], 3], 4]
        )

    def test_two(self):
        self.run_explode_test(
            [7,[6,[5,[4,[3,2]]]]],
            [7,[6,[5,[7,0]]]]
        )

    def test_three(self):
        self.run_explode_test(
            [[6,[5,[4,[3,2]]]],1],
            [[6,[5,[7,0]]],3]
        )

    def test_four(self):
        self.run_explode_test(
            [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]],
            [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
        )

    def test_five(self):
        self.run_explode_test(
            [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]],
            [[3,[2,[8,0]]],[9,[5,[7,0]]]]
        )

    def test_six(self):
        self.run_explode_test(
            [[[[0, 7], 4], [7, [[8, 4], 9]]], [1, 1]],
            [[[[0,7],4],[15,[0,13]]],[1,1]]
        )

    def test_seven(self):
        self.run_explode_test(
            [[[[[1, 1], [2, 2]], [3, 3]], [4, 4]], [5, 5]],
            [[[[0, [3, 2]], [3, 3]], [4, 4]], [5, 5]]
        )

    def test_eight(self):
        self.run_explode_test(
            [[[[0, [3, 2]], [3, 3]], [4, 4]], [5, 5]],
            [[[[3, 0], [5, 3]], [4, 4]], [5, 5]]
        )


class TestSplit(unittest.TestCase):

    def run_split_test(self, input, expected_result):
        result, _ = try_split(input)
        self.assertEqual(expected_result, result)

    def test_one(self):
        self.run_split_test(
            10,
            [5, 5]
        )

    def test_two(self):
        self.run_split_test(
            11,
            [5, 6]
        )

    def test_three(self):
        self.run_split_test(
            12,
            [6, 6]
        )

    def test_four(self):
        self.run_split_test(
            [[[[0,7],4],[15,[0,13]]],[1,1]],
            [[[[0,7],4],[[7,8],[0,13]]],[1,1]]
        )

    def test_five(self):
        self.run_split_test(
            [[[[0,7],4],[[7,8],[0,13]]],[1,1]],
            [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]
        )


class TestReduce(unittest.TestCase):

    def run_reduce_test(self, input, expected_result):
        result = reduce_snailfish(input)
        self.assertEqual(expected_result, result)

    def test_one(self):
        self.run_reduce_test(
            [[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]],
            [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
        )

    def test_two(self):
        self.run_reduce_test(
            [[[[[1,1],[2,2]],[3,3]],[4,4]], [5,5]],
            [[[[3,0],[5,3]],[4,4]],[5,5]]
        )


class TestAdd(unittest.TestCase):

    def run_sum_test(self, input, expected_result):
        result = sum_snailfish(input)
        self.assertEqual(expected_result, result)

    def test_one(self):
        self.run_sum_test(
            [
                [[[[4, 3], 4], 4], [7, [[8, 4], 9]]],
                [1, 1]
            ],
            [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
        )

    def test_two(self):
        self.run_sum_test(
            [
                [1, 1],
                [2, 2],
                [3, 3],
                [4, 4],
            ],
            [[[[1,1],[2,2]],[3,3]],[4,4]]
        )

    def test_three(self):
        self.run_sum_test(
            [
                [1, 1],
                [2, 2],
                [3, 3],
                [4, 4],
                [5, 5],
            ],
            [[[[3,0],[5,3]],[4,4]],[5,5]]
        )

    def test_four(self):
        self.run_sum_test(
            [
                [[[[1,1],[2,2]],[3,3]],[4,4]],
                [5,5],
            ],
            [[[[3, 0], [5, 3]], [4, 4]], [5, 5]]
        )

    def test_last(self):
        self.run_sum_test(
            [
                [[[0, [5, 8]], [[1, 7], [9, 6]]], [[4, [1, 2]], [[1, 4], 2]]],
                [[[5, [2, 8]], 4], [5, [[9, 9], 0]]],
                [6, [[[6, 2], [5, 6]], [[7, 6], [4, 7]]]],
                [[[6, [0, 7]], [0, 9]], [4, [9, [9, 0]]]],
                [[[7, [6, 4]], [3, [1, 3]]], [[[5, 5], 1], 9]],
                [[6, [[7, 3], [3, 2]]], [[[3, 8], [5, 7]], 4]],
                [[[[5, 4], [7, 7]], 8], [[8, 3], 8]],
                [[9, 3], [[9, 9], [6, [4, 9]]]],
                [[2, [[7, 7], 7]], [[5, 8], [[9, 3], [0, 2]]]],
                [[[[5, 2], 5], [8, [3, 7]]], [[5, [7, 5]], [4, 4]]],
            ],
            [[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]
        )



class TestMagnitude(unittest.TestCase):

    def run_mag_test(self, test_input, expected_result):
        result = calc_magnitude(test_input)
        self.assertEqual(expected_result, result)

    def test_one(self):
        self.run_mag_test([[1, 2], [[3, 4], 5]], 143)

    def test_second_last(self):
        self.run_mag_test([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]], 3488)

    def test_last(self):
        self.run_mag_test([[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]], 4140)

if __name__ == '__main__':
    unittest.main()
