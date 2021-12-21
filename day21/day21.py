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
    data = advent_tools.read_all_integers()
    # data = advent_tools.read_whole_input()
    # data = advent_tools.read_input_lines()
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
    p1start = data[0][1]
    p2start = data[1][1]
    return p1start, p2start


def get_roll(roll_num, player_num):
    a = 9 * player_num - 3
    return 18 * roll_num + a

def get_points(roll_num, player_num, start):
    s = sum(get_roll(i, player_num) for i in range(roll_num + 1)) + start
    return (s - 1) % 10 + 1



def run_part_1(data):
    start1, start2 = data
    points1 = {i: get_points(i, 1, start1) for i in range(10)}
    points2 = {i: get_points(i, 2, start2) for i in range(10)}
    ten_points1 = sum(points1.values())
    ten_points2 = sum(points2.values())
    sum1 = 0
    sum2 = 0
    rolls = 0
    while sum1 + ten_points1 < 1000 and sum2 + ten_points2 < 1000:
        rolls += 10
        sum1 += ten_points1
        sum2 += ten_points2
    rolls1 = rolls2 = rolls - 1
    while sum1 < 1000 and sum2 < 1000:
        rolls1 += 1
        sum1 += points1[rolls1 % 10]
        if sum1 < 1000:
            rolls2 += 1
            sum2 += points2[rolls2 % 10]
    return 3 * min(sum1, sum2) * (rolls1 + rolls2 + 2)


def run_part_2(data):
    start1, start2 = data
    sums = [sum([roll1, roll2, roll3])
            for roll1, roll2, roll3 in itertools.product(range(1, 4), repeat=3)]
    counts = collections.Counter(sums)
    results = {(start1, 0, start2, 0): 1}
    win1 = 0
    win2 = 0
    rolls = 0
    while results:
        rolls += 1
        new_results = collections.defaultdict(int)
        for p1_roll_sum, p1_count in counts.items():
            for (p1_spot, p1_points, p2_spot, p2_points), count in results.items():
                new_p1_spot = (p1_spot + p1_roll_sum - 1) % 10 + 1
                new_p1_points = p1_points + new_p1_spot
                if new_p1_points >= 21:
                    win1 += count * p1_count
                else:
                    new_results[(new_p1_spot, new_p1_points, p2_spot, p2_points)] += count * p1_count
        results = {**new_results}
        new_results = collections.defaultdict(int)
        for p2_roll_sum, p2_count in counts.items():
            for (p1_spot, p1_points, p2_spot, p2_points), count in results.items():
                new_p2_spot = (p2_spot + p2_roll_sum - 1) % 10 + 1
                new_p2_points = p2_points + new_p2_spot
                if new_p2_points >= 21:
                    win2 += count * p2_count
                else:
                    new_results[(p1_spot, p1_points, new_p2_spot, new_p2_points)] += count * p2_count
        results = {**new_results}
    return max(win1, win2)



if __name__ == '__main__':
    main()
