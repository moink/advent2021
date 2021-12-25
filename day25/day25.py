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


def run_part_1(state):
    gcf = plt.gcf()
    gca = plt.gca()
    gca.set_axis_off()
    camera = Camera(gcf)
    old_data = np.zeros_like(state.grid)
    count = 0
    while (old_data != state.grid).any().any():
        count += 1
        old_data = state.grid.copy()
        move_one_step(state, EAST_FACING, 1)
        move_one_step(state, SOUTH_FACING, 0)
        state.imshow_grid()
        camera.snap()
    animation = camera.animate()
    animation.save("animated_cucumbers.gif")
    return count


def move_one_step(current_state, direction, axis):
    facing_direction = current_state.grid == direction
    empty = current_state.grid == EMPTY
    move_into = np.roll(facing_direction, 1, axis) & empty
    move_from = np.roll(move_into, -1, axis)
    current_state.grid[move_into] = direction
    current_state.grid[move_from] = EMPTY


if __name__ == '__main__':
    main()
