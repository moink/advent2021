import pandas as pd

import advent_tools


def main():
    data = advent_tools.read_one_int_per_line()
    data = process_input(data)
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def process_input(data):
    return pd.Series(data)


def run_part_1(data):
    return sum(data.diff() > 0)


def run_part_2(data):
    rolling = data.rolling(3).sum()
    return sum(rolling.diff() > 0)


if __name__ == '__main__':
    main()
