import collections
import itertools
import re
import time

import numpy as np

import advent_tools

MIN_BEACON_OVERLAP = 12


def main():
    start_time = time.perf_counter()
    data = process_input(advent_tools.read_input_line_groups())
    part1, part2 = run_both_parts(data)
    print('Part 1:', part1)
    print('Part 2:', part2)
    print("Elapsed time", time.perf_counter() - start_time)


def process_input(data):
    return [[np.asarray([int(num_str) for num_str in (re.findall(r'-?[0-9]+', line))])
             for line in chunk[1:]] for chunk in data]


def all_orientations(scanner):
    for dir_x, dir_y in itertools.permutations(range(3), 2):
        for sign_x, sign_y in itertools.product((-1, 1), (-1, 1)):
            x_vec = np.zeros((3,))
            y_vec = np.zeros((3,))
            x_vec[dir_x] = sign_x
            y_vec[dir_y] = sign_y
            z_vec = np.cross(x_vec, y_vec)
            yield [
                (np.asarray((
                    np.dot(x_vec, beacon),
                    np.dot(y_vec, beacon),
                    np.dot(z_vec, beacon),
                ))) for beacon in scanner]


def find_all_distances(scanner1, scanner2):
    return [tuple((beacon2 - beacon1).astype(int))
            for beacon1, beacon2 in itertools.product(scanner1, scanner2)]


def manhattan_distance(scanner_pos1, scanner_pos2):
    return sum(abs(s2 - s1) for s1, s2 in zip(scanner_pos1, scanner_pos2))


def run_both_parts(all_scanners):
    unsolved_scanners = set(range(1, len(all_scanners)))
    solved_scanners = collections.deque([0])
    scanner_beacons = {0: {tuple(beacon) for beacon in all_scanners[0]}}
    scanner_positions = [(0, 0, 0)]
    while unsolved_scanners:
        known_scanner = solved_scanners.pop()
        unsolved_scanners = set(range(len(all_scanners))).difference(
            scanner_beacons.keys())
        for scanner_num in unsolved_scanners:
            for oriented_scanner in all_orientations(all_scanners[scanner_num]):
                distances = find_all_distances(scanner_beacons[known_scanner],
                                               oriented_scanner)
                for shift, count in collections.Counter(distances).items():
                    if count >= MIN_BEACON_OVERLAP:
                        scanner_beacons[scanner_num] = {
                            tuple((beacon1 - shift).astype(int))
                            for beacon1 in oriented_scanner
                        }
                        solved_scanners.append(scanner_num)
                        scanner_positions.append(tuple(shift))
    num_beacons = len({beacon for grid in scanner_beacons.values() for beacon in grid})
    max_distance = int(max(manhattan_distance(shift1, shift2)
                           for shift1, shift2
                           in itertools.combinations(scanner_positions, 2)))
    return num_beacons, max_distance


if __name__ == '__main__':
    main()