import collections
import math

import numpy as np

import advent_tools


def main():
    heights = advent_tools.read_nparray_from_digits()
    low_points = find_low_points(heights)
    print('Part 1:', run_part_1(heights, low_points))
    print('Part 2:', run_part_2(heights, low_points))


def run_part_1(heights, low_points):
    low_values = heights[low_points]
    return sum(low_values) + len(low_values)


def find_low_points(heights):
    diff_x = np.diff(heights, axis=1)
    less_than_right = np.pad(diff_x, ((0, 0), (1, 0)),
                             "constant", constant_values=((0, 0), (-1, 0))) < 0
    less_than_left = np.pad(diff_x, ((0, 0), (0, 1)),
                            "constant", constant_values=((0, 0), (0, 1))) > 0
    diff_y = np.diff(heights, axis=0)
    less_than_below = np.pad(diff_y, ((1, 0), (0, 0)),
                             "constant", constant_values=((-1, 0), (0, 0))) < 0
    less_than_above = np.pad(diff_y, ((0, 1), (0, 0)),
                             "constant", constant_values=((0, 1), (0, 0))) > 0
    low_points = less_than_right & less_than_left & less_than_below & less_than_above
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

    not_evaluated = collections.deque(basin)
    while not_evaluated:
        y, x = not_evaluated.pop()
        for new_pos in [(y, x - 1), (y, x + 1), (y - 1, x), (y + 1, x)]:
            if belongs_to_basin(new_pos):
                basin.add(new_pos)
                not_evaluated.append(new_pos)
    return basin


if __name__ == '__main__':
    main()