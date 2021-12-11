import numpy as np
from scipy import signal

import advent_tools


def main():
    data = advent_tools.read_nparray_from_digits()
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def run_part_1(energy):
    flash_count = 0
    n_steps = 100
    convolve_matrix = np.ones((3, 3))
    convolve_matrix[1, 1] = 0
    for step in range(n_steps):
        energy = energy + 1
        flashes = energy > 9
        need_to_continue = True
        while need_to_continue:
            neighbour_flashes = signal.convolve(flashes, convolve_matrix, mode='same').round(0).astype(int)
            new_energy = energy + neighbour_flashes
            new_flashes = new_energy > 9
            need_to_continue = (new_flashes & ~flashes).sum().sum() > 0
            flashes = new_flashes
        energy = new_energy
        energy[flashes] = 0
        flash_count += new_flashes.sum().sum()
    return flash_count

def run_part_2(energy):
    n_steps = 1000
    convolve_matrix = np.ones((3, 3))
    convolve_matrix[1, 1] = 0
    for step in range(n_steps):
        energy = energy + 1
        flashes = energy > 9
        need_to_continue = True
        while need_to_continue:
            neighbour_flashes = signal.convolve(flashes, convolve_matrix, mode='same').round(0).astype(int)
            new_energy = energy + neighbour_flashes
            new_flashes = new_energy > 9
            need_to_continue = (new_flashes & ~flashes).sum().sum() > 0
            flashes = new_flashes
        energy = new_energy
        energy[flashes] = 0
        if flashes.all().all():
            return step + 1


if __name__ == '__main__':
    main()