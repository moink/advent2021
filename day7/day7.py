import math
import statistics

import advent_tools


def main():
    data = advent_tools.read_all_integers()[0]
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def run_part_1(data):
    med = statistics.median(data)
    return int(sum(math.fabs(d-med) for d in data))


def run_part_2(data):
    mean = statistics.mean(data)
    fuel1 = sum(get_fuel(abs(int(math.floor(mean)) - d)) for d in data)
    fuel2 = sum(get_fuel(abs(int(math.ceil(mean)) - d)) for d in data)
    return min(fuel1, fuel2)


def get_fuel(dist):
    return dist * (dist + 1) // 2


if __name__ == '__main__':
    main()
