import numpy as np

import advent_tools
from advent_tools import shift_with_padding


def main():
    risk_level = advent_tools.read_nparray_from_digits()
    print('Part 1:', run_part_1(risk_level))
    print('Part 2:', run_part_2(risk_level))


def run_part_1(risk_level):
    return find_min_path(risk_level)


def run_part_2(risk_level):
    return find_min_path(
        np.block([[(risk_level + row + col - 1) % 9 + 1 for col in range(5)]
                  for row in range(5)]))


def find_min_path(risk_level):
    big_number = risk_level.sum().sum()
    cost = big_number * np.ones_like(risk_level)
    cost[-1, -1] = risk_level[-1, -1]
    not_converged = True
    while not_converged:
        old_cost = cost
        cost = np.minimum.reduce([
            cost,
            risk_level + shift_with_padding(cost, -1, 0, big_number),
            risk_level + shift_with_padding(cost, 1, 0, big_number),
            risk_level + shift_with_padding(cost, -1, 1, big_number),
            risk_level + shift_with_padding(cost, 1, 1, big_number)
        ])
        not_converged = np.abs(cost - old_cost).any().any()
    return cost[0, 0] - risk_level[0, 0]


if __name__ == '__main__':
    main()
