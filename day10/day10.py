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
    # data = advent_tools.read_nparray_from_digits()
    data = process_input(data)
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def process_input(data):
    return data


def run_part_1(data):
    brace_chars = {
        "{": "}",
        "(": ")",
        "[": "]",
        "<": ">",
    }
    bad_chars = []
    for line in data:
        currently_in = []
        for char in line:
            if char in brace_chars:
                currently_in.append(char)
            elif char == brace_chars[currently_in[-1]]:
                currently_in.pop(-1)
            else:
                bad_chars.append(char)
                break
    counts = collections.Counter(bad_chars)
    costs = {
        "}": 1197,
        ")": 3,
        "]": 57,
        ">": 25137,
    }
    return sum(v*costs[k] for k, v in counts.items())


def score_line(completion):
    brace_chars = {
        "}": 3,
        ")": 1,
        "]": 2,
        ">": 4,
    }
    score = 0
    for char in completion:
        num = brace_chars[char]
        score = 5 * score + num
    return score

def run_part_2(data):
    brace_chars = {
        "{": "}",
        "(": ")",
        "[": "]",
        "<": ">",
    }
    scores = []
    for line in data:
        completion = get_completion(brace_chars, line)
        if completion:
            scores.append(score_line(completion))
    return statistics.median(scores)


def get_completion(brace_chars, line):
    currently_in = []
    for char in line:
        if char in brace_chars:
            currently_in.append(char)
        elif char == brace_chars[currently_in[-1]]:
            currently_in.pop(-1)
        elif char in brace_chars.values():
            return ""
    else:
        completion = "".join(brace_chars[char] for char in reversed(currently_in))
    return completion


if __name__ == '__main__':
    main()