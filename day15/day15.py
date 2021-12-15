import numpy as np

import advent_tools


def main():
    risk_level = advent_tools.read_nparray_from_digits()
    print('Part 1:', run_part_1(risk_level))
    print('Part 2:', run_part_2(risk_level))


def run_part_1(risk_level):
    return find_min_path(risk_level)


def run_part_2(risk_level):
    return find_min_path(
        np.concatenate(
            [np.concatenate(
                [np.mod(risk_level + i + j - 1, 9) + 1 for j in range(5)], 1)
                for i in range(5)], 0))


def find_min_path(risk_level):
    big_number = risk_level.sum().sum()
    cost = big_number * np.ones_like(risk_level)
    cost[- 1, - 1] = risk_level[- 1, - 1]
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


def shift_with_padding(data, shift, axis, pad_value):
    shifted_data = np.roll(data, shift, axis=axis)
    null_slice = slice(None, None)
    if shift < 0:
        part_slice = slice(shift, None)
    else:
        part_slice = slice(None, shift)
    if axis == 1:
        full_slice = (null_slice, part_slice)
    else:
        full_slice = (part_slice, null_slice)
    shifted_data[full_slice] = pad_value
    return shifted_data


if __name__ == '__main__':
    main()
