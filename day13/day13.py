import numpy as np
from matplotlib import pyplot as plt

import advent_tools


def main():
    grid_part, fold_part = advent_tools.read_input_line_groups()
    grid = make_initial_grid(grid_part)
    folds = preprocess_folds(fold_part)
    print('Part 1:', run_part_1(grid, folds))
    run_part_2(grid, folds)


def make_initial_grid(grid_part):
    max_x = max(int(line.split(",")[0]) for line in grid_part)
    max_y = max(int(line.split(",")[1]) for line in grid_part)
    grid = np.zeros((max_y + 1, max_x + 1), dtype=bool)
    for line in grid_part:
        x, y = line.split(",")
        grid[int(y), int(x)] = True
    return grid


def preprocess_folds(fold_part):
    axis_map = {"x": 1, "y": 0}
    folds = []
    for line in fold_part:
        equation = line.split()[-1]
        axis, pos = equation.split("=")
        folds.append((axis_map[axis], int(pos)))
    return folds


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
    plt.title("Part 2")
    plt.show()


if __name__ == '__main__':
    main()
