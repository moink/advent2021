import numpy as np
from celluloid import Camera
from matplotlib import pyplot as plt

import advent_tools

EMPTY = 0
EAST_FACING = 1
SOUTH_FACING = 2


def main():
    data = advent_tools.PlottingGrid.from_file(
        {'.' : EMPTY, '>' : EAST_FACING, 'v': SOUTH_FACING}
    )
    print('Part 1:', run_part_1(data))


def run_part_1(data):
    gcf = plt.gcf()
    gca = plt.gca()
    gca.set_axis_off()
    camera = Camera(gcf)
    old_data = np.zeros_like(data.grid)
    count = 0
    while (old_data != data.grid).any().any():
        count += 1
        old_data = data.grid.copy()
        move_one_step(data, EAST_FACING, 1)
        move_one_step(data, SOUTH_FACING, 0)
        data.imshow_grid()
        camera.snap()
    animation = camera.animate()
    animation.save("animated_cucumbers.gif")
    return count


def move_one_step(data, direction, axis):
    east_facing = data.grid == direction
    empty = data.grid == EMPTY
    moved_right = np.roll(east_facing, 1, axis)
    move_into = moved_right & empty
    move_from = np.roll(move_into, -1, axis)
    data.grid[move_into] = direction
    data.grid[move_from] = EMPTY


if __name__ == '__main__':
    main()
