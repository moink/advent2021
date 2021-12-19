import collections
import itertools
import re
import time

import numpy as np

import advent_tools

MIN_BEACON_OVERLAP = 12


def main():
    start_time = time.perf_counter()
    scanner_readings = process_input(advent_tools.read_input_line_groups())
    part1, part2 = run_both_parts(scanner_readings)
    print('Part 1:', part1)
    print('Part 2:', part2)
    print("Elapsed time", time.perf_counter() - start_time)


def process_input(data):
    return [[np.asarray([int(num_str) for num_str in (re.findall(r'-?[0-9]+', line))])
             for line in chunk[1:]] for chunk in data]


def run_both_parts(scanner_readings):
    absolute_beacons = {tuple(beacon) for beacon in scanner_readings[0]}
    scanner_positions = {(0, 0, 0)}
    solved_scanners = {0}
    all_scanners = set(range(1, len(scanner_readings)))
    unsolved_scanners = all_scanners
    while unsolved_scanners:
        unsolved_scanners = all_scanners.difference(solved_scanners)
        for scanner_num in unsolved_scanners:
            solved, distance, abs_beacons = match_scanners(
                absolute_beacons, scanner_readings[scanner_num]
            )
            if solved:
                solved_scanners.add(scanner_num)
                scanner_positions.add(distance)
                absolute_beacons = absolute_beacons.union(abs_beacons)
    max_distance = int(max(manhattan_distance(shift1, shift2)
                           for shift1, shift2
                           in itertools.combinations(scanner_positions, 2)))
    return len(absolute_beacons), max_distance


def match_scanners(known_absolute_beacons, unknown_scanner_readings):
    for oriented_scanner in all_orientations(unknown_scanner_readings):
        distances = find_all_distances(known_absolute_beacons,
                                       oriented_scanner)
        for distance, count in collections.Counter(distances).items():
            if count >= MIN_BEACON_OVERLAP:
                absolute_beacons = {
                    tuple((beacon1 - distance).astype(int))
                    for beacon1 in oriented_scanner
                }
                return True, tuple(distance), absolute_beacons
    return False, None, None


def all_orientations(scanner):
    for dir_x, dir_y in itertools.permutations(range(3), 2):
        for sign_x, sign_y in itertools.product((-1, 1), repeat=2):
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


if __name__ == '__main__':
    main()