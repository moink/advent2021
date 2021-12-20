import numpy as np
from scipy import signal

import advent_tools


def main():
    data = advent_tools.read_nparray_from_digits()
    part1, part2 = run_both_parts(data)
    print('Part 1:', part1)
    print('Part 2:', part2)


def run_both_parts(energy):
    new_energy = energy
    part1_sol = 0
    flash_count = 0
    convolve_matrix = np.ones((3, 3))
    step = 0
    while True:
        step = step + 1
        energy = energy + 1
        flashes = energy > 9
        have_new_flashes = True
        while have_new_flashes:
            neighbour_flashes = (signal.convolve(flashes, convolve_matrix, mode='same')
                                 .round(0).astype(int))
            new_energy = energy + neighbour_flashes
            new_flashes = new_energy > 9
            have_new_flashes = (new_flashes & ~flashes).sum().sum() > 0
            flashes = new_flashes
        energy = new_energy
        energy[flashes] = 0
        flash_count += flashes.sum().sum()
        if step == 100:
            part1_sol = flash_count
        if flashes.all().all():
            return part1_sol, step


if __name__ == '__main__':
    main()
