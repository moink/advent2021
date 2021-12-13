import numpy as np
from matplotlib import pyplot as plt

import advent_tools


def main():
    data = advent_tools.read_input_line_groups()
    grid, folds = process_input(data)
    print('Part 1:', run_part_1(grid, folds))
    run_part_2(grid, folds)


def process_input(data):
    max_x = max(int(line.split(",")[0]) for line in data[0])
    max_y = max(int(line.split(",")[1]) for line in data[0])
    grid = np.zeros((max_y + 1, max_x + 1), dtype=bool)
    for line in data[0]:
        x, y = line.split(",")
        grid[int(y), int(x)] = True
    folds = []
    for line in data[1]:
        equation = line.split()[-1]
        axis, pos = equation.split("=")
        if axis == "x":
            folds.append((1, int(pos)))
        else:
            folds.append((0, int(pos)))
    return grid, folds


def fold_grid(grid, axis, pos):
    if axis == 0:
        grid1 = grid[0: pos, :]
        grid2 = grid[pos + 1:, :]
    else:
        grid1 = grid[:, 0: pos]
        grid2 = grid[:, pos + 1:]
    result = grid1 | np.flip(grid2, axis=axis)
    return result


def run_part_1(grid, folds):
    return fold_grid(grid, folds[0][0], folds[0][1]).sum().sum()


def run_part_2(grid, folds):
    for axis, pos in folds:
        grid = fold_grid(grid, axis, pos)
    plt.imshow(grid)
    plt.show()


if __name__ == '__main__':
    main()