import numpy as np
import advent_tools


def main():
    data = advent_tools.read_all_integers()
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def run_part_1(data):
    grid = np.zeros((1000, 1000))
    for x0, y0, x1, y1 in data:
        if x0 == x1:
            grid[x0, min(y0, y1):max(y0, y1) + 1] += 1
        if y0 == y1:
            grid[min(x0, x1):max(x0, x1) + 1, y0] += 1
    return (grid >= 2).sum().sum()


def run_part_2(data):
    grid = np.zeros((1000, 1000))
    for x0, y0, x1, y1 in data:
        if x0 == x1:
            grid[x0, min(y0, y1):max(y0, y1) + 1] += 1
        elif y0 == y1:
            grid[min(x0, x1):max(x0, x1) + 1, y0] += 1
        else:
            xrange = list(range(x0, x1 + 1)) or list(range(x0, x1 - 1, -1))
            yrange = list(range(y0, y1 + 1)) or list(range(y0, y1 - 1, -1))
            for x, y in zip(xrange, yrange):
                grid[x, y] += 1
    return (grid >= 2).sum().sum()


if __name__ == '__main__':
    main()
