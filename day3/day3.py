import contextlib
import collections
import copy
import functools
import itertools
import math
import sys

import numpy as np
import pandas as pd
import re

import advent_tools


def main():
    # advent_tools.TESTING = True
    # raw_data = advent_tools.read_all_integers()
    # raw_data = advent_tools.read_whole_input()
    raw_data = advent_tools.read_input_lines()
    # raw_data = advent_tools.read_input_no_strip()
    # raw_data = advent_tools.read_dict_from_input_file(sep=' => ', key='left')
    # raw_data = advent_tools.read_dict_of_list_from_file(sep=' => ', key='left')
    # raw_data = advent_tools.read_one_int_per_line()
    # raw_data = advent_tools.PlottingGrid.from_file({'.' : 0, '#' : 1})
    # raw_data = advent_tools.read_input_line_groups()
    data = process_input(raw_data)
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(raw_data, data))


def process_input(data):
    return list(map(list, itertools.zip_longest(*data)))


def run_part_1(data):
    delta_bits = []
    eps_bits = []
    for pos in zip(data):
        if pos[0].count("1") > pos[0].count("0"):
            delta_bits.append("1")
            eps_bits.append("0")
        else:
            delta_bits.append("0")
            eps_bits.append("1")
    delta = int("".join(delta_bits), 2)
    eps = int("".join(eps_bits), 2)
    return delta * eps


def run_part_2(raw_data, data):
    ox = int(get_oxygen_gen(raw_data, 0)[0], 2)
    co2 = int(get_co2_scrubber(raw_data, 0)[0], 2)
    return ox * co2


def get_oxygen_gen(raw_data, pos):
    pos = pos % len(raw_data[0])
    if len(raw_data) == 1:
        return raw_data
    pos_vals = [line[pos] for line in raw_data]
    if pos_vals.count("1") >= pos_vals.count("0"):
        new_data = [line for line in raw_data if line[pos]=="1"]
    else:
        new_data = [line for line in raw_data if line[pos]=="0"]
    return get_oxygen_gen(new_data, pos + 1)

def get_co2_scrubber(raw_data, pos):
    pos = pos % len(raw_data[0])
    if len(raw_data) == 1:
        return raw_data
    pos_vals = [line[pos] for line in raw_data]
    if pos_vals.count("1") >= pos_vals.count("0"):
        new_data = [line for line in raw_data if line[pos] == "0"]
    else:
        new_data = [line for line in raw_data if line[pos] == "1"]
    return get_co2_scrubber(new_data, pos + 1)

if __name__ == '__main__':
    main()