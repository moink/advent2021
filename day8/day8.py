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
    data = advent_tools.read_input_lines()
    # data = advent_tools.read_input_no_strip()
    # data = advent_tools.read_dict_from_input_file(sep=' => ', key='left')
    # data = advent_tools.read_dict_of_list_from_file(sep=' => ', key='left')
    # data = advent_tools.read_one_int_per_line()
    # data = advent_tools.PlottingGrid.from_file({'.' : 0, '#' : 1})
    # data = advent_tools.read_input_line_groups()
    # data = process_input(data)
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def run_part_1(data):
    p = get_counts(data)
    return p[2] + p[3] + p[4] + p[7]


def get_counts(data):
    counts = []
    for line in data:
        left, right = line.split("|")
        all_c = right.split()
        for word in all_c:
            c = collections.Counter(word)
            counts.append(len(c))
    p = collections.Counter(counts)
    return p


def run_part_2(data):
    result = 0
    for line in data:
        left, right = line.split("|")
        all_c = left.split()
        number_map = get_number_map(all_c)
        print(number_map)
        digits = []
        for word in right.split():
            key = "".join(sorted(word))
            print(key)
            digits.append(number_map[key])
        result += int("".join(digits))
    return result

def get_number_map(all_c):
    unique = set()
    for word in all_c:
        unique.add("".join(sorted(word)))
    result_map = {}
    result_map["1"] = get_that_matches(unique, lambda x: len(x) == 2)
    result_map["4"] = get_that_matches(unique, lambda x: len(x) == 4)
    result_map["7"] = get_that_matches(unique, lambda x: len(x) == 3)
    result_map["8"] = get_that_matches(unique, lambda x: len(x) == 7)
    result_map["3"] = get_that_matches(unique, lambda x: len(x) == 5 and all(char in x for char in result_map["1"]))
    result_map["9"] = get_that_matches(unique, lambda x: len(x) == 6 and all(char in x for char in result_map["4"]))
    result_map["0"] = get_that_matches(unique, lambda x: len(x) == 6 and all(char in x for char in result_map["1"]))
    result_map["6"] = get_that_matches(unique, lambda x: len(x) == 6)
    result_map["5"] = get_that_matches(unique, lambda x: len(x) == 5 and all(char in result_map["6"] for char in x))
    result_map["2"] = get_that_matches(unique, lambda x: len(x) == 5)
    return {val: key for key, val in result_map.items()}


def get_that_matches(not_found_yet, fun):
    for val in not_found_yet:
        if fun(val):
            not_found_yet.remove(val)
            return val
    raise RuntimeError("No matching value")

if __name__ == '__main__':
    main()