import contextlib
import collections
import copy
import functools
import itertools
import math
import re
import statistics

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import advent_tools


def main():
    # advent_tools.TESTING = True
    # data = advent_tools.read_all_integers()
    # data = advent_tools.read_whole_input()
    # data = advent_tools.read_input_lines()
    # data = advent_tools.read_input_no_strip()
    data = advent_tools.read_dict_from_input_file(sep=' -> ', key='left')
    # data = advent_tools.read_dict_of_list_from_file(sep=' => ', key='left')
    # data = advent_tools.read_one_int_per_line()
    # data = advent_tools.PlottingGrid.from_file({'.' : 0, '#' : 1})
    # data = advent_tools.read_input_line_groups()
    # data = advent_tools.read_nparray_from_digits()
    if advent_tools.TESTING:
        start = "NNCB"
    else:
        start = "OFSVVSFOCBNONHKFHNPK"
    print('Part 1:', run_part(start, data, 10))
    print('Part 2:', run_part(start, data, 40))


def run_part(polymer, data, steps):
    pair_counts = collections.defaultdict(int)
    char_counts = collections.defaultdict(int, collections.Counter(polymer))
    for first_char, second_char in zip(polymer[:-1], polymer[1:]):
        pair_counts["".join((first_char, second_char))] +=1
    for _ in range(steps):
        new_pair_counts = collections.defaultdict(int)
        for pair, count in pair_counts.items():
            between = data[pair]
            first_char, second_char = pair
            new_pair_counts["".join((first_char, between))] += count
            new_pair_counts["".join((between, second_char))] += count
            char_counts[between] += count
        pair_counts = new_pair_counts
    return max(char_counts.values()) - min(char_counts.values())
    # not 4302675529691

if __name__ == '__main__':
    main()