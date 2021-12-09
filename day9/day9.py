import collections
import math

import numpy as np

import advent_tools


def main():
    data = advent_tools.read_input_lines()
    data = process_input(data)
    low_points = find_low_points(data)
    print('Part 1:', run_part_1(data, low_points))
    print('Part 2:', run_part_2(data, low_points))


def process_input(data):
    result = np.zeros((len(data), len(data[0])), dtype=int)
    for i, line in enumerate(data):
        for j, char in enumerate(line):
            result[i, j] = int(char)
    return result


def run_part_1(data, low_points):
    low_values = data[low_points]
    return sum(low_values) + len(low_values)


def find_low_points(data):
    diff_x = np.diff(data, axis=1)
    d1 = np.pad(diff_x, ((0, 0), (1, 0)),
                "constant", constant_values=((0, 0), (-1, 0))) < 0
    d2 = np.pad(diff_x, ((0, 0), (0, 1)),
                "constant", constant_values=((0, 0), (0, 1))) > 0
    diff_y = np.diff(data, axis=0)
    d3 = np.pad(diff_y, ((1, 0), (0, 0)),
                "constant", constant_values=((-1, 0), (0, 0))) < 0
    d4 = np.pad(diff_y, ((0, 1), (0, 0)),
                "constant", constant_values=((0, 1), (0, 0))) > 0
    low_points = d1 & d2 & d3 & d4
    return low_points


def run_part_2(data, low_points):
    y_coords, x_coords = np.where(low_points)
    basin_sizes = []
    for x, y in zip(x_coords, y_coords):
        basin = get_basin(data, x, y)
        basin_sizes.append(len(basin))
    return math.prod(sorted(basin_sizes, reverse=True)[0:3])


def get_basin(data, start_x, start_y):
    max_y, max_x = data.shape
    basin = {(start_y, start_x)}

    def belongs_to_basin(pos):
        yy, xx = pos
        return (0 < xx < max_x and 0 < yy < max_y and pos not in basin
                and data[pos] != 9)

    not_evaluated = collections.deque([(start_y, start_x)])
    while not_evaluated:
        y, x = not_evaluated.pop()
        to_consider = [(y, x - 1), (y, x + 1), (y - 1, x), (y + 1, x)]
        for new_pos in to_consider:
            if belongs_to_basin(new_pos):
                basin.add(new_pos)
                not_evaluated.append(new_pos)
    return basin


if __name__ == '__main__':
    main()