import numpy as np

import advent_tools


def main():
    data = advent_tools.read_nparray_from_digits().astype(float)
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def run_part_1(data):
    return find_min_path(data)


def run_part_2(data):
    return find_min_path(
        np.concatenate(
            [np.concatenate(
                [np.mod(data + i + j - 1, 9) + 1 for j in range(5)], 1)
             for i in range(5)], 0))


def find_min_path(data):
    cost = np.inf * np.ones_like(data)
    max_y, max_x = data.shape
    cost[max_y - 1, max_x - 1] = data[max_y - 1, max_x - 1]
    keep_going = True
    while keep_going:
        old_cost = cost
        cost = np.minimum(cost, data + roll_inf_pad(cost, -1, 0))
        cost = np.minimum(cost, data + roll_inf_pad(cost, 1, 0))
        cost = np.minimum(cost, data + roll_inf_pad(cost, -1, 1))
        cost = np.minimum(cost, data + roll_inf_pad(cost, 1, 1))
        keep_going = np.abs(cost - old_cost).any().any()
    return int(cost[0, 0] - data[0, 0])


def roll_inf_pad(data, shift, axis):
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
    shifted_data[full_slice] = np.inf
    return shifted_data



if __name__ == '__main__':
    main()