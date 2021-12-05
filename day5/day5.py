import numpy as np
import advent_tools


def main():
    data = advent_tools.read_all_integers()
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def run_part_1(data):
    return get_intersection_count(data, False)


def run_part_2(data):
    return get_intersection_count(data, True)


def get_intersection_count(data, consider_diag):
    grid = np.zeros((1000, 1000))
    for x0, y0, x1, y1 in data:
        if x0 == x1:
            grid[x0, get_range(y0, y1)] += 1
        elif y0 == y1:
            grid[get_range(x0, x1), y0] += 1
        elif consider_diag:
            for x, y in zip(get_range(x0, x1), get_range(y0, y1)):
                grid[x, y] += 1
    return (grid >= 2).sum().sum()


def get_range(x0, x1):
    return range(x0, x1 + 1) or range(x0, x1 - 1, -1)


if __name__ == '__main__':
    main()
