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
from advent_tools import read_input_lines


def main():
    # advent_tools.TESTING = True
    # data = advent_tools.read_all_integers()
    # data = advent_tools.read_whole_input()
    # data = advent_tools.read_input_lines()
    # data = advent_tools.read_input_no_strip()
    data = []
    lines = read_input_lines()
    for line in lines:
        left, right = line.split('-')
        data.append((left.strip(), right.strip()))
        data.append((right.strip(), left.strip()))
    # data = advent_tools.read_dict_of_list_from_file(sep=' => ', key='left')
    # data = advent_tools.read_one_int_per_line()
    # data = advent_tools.PlottingGrid.from_file({'.' : 0, '#' : 1})
    # data = advent_tools.read_input_line_groups()
    # data = advent_tools.read_nparray_from_digits()
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


class MazeState(advent_tools.StateForGraphs):

    def __init__(self, maze, nodes):
        self.nodes = nodes
        self.maze = maze

    def __str__(self):
        return "_".join(self.nodes)

    def is_final(self):
        return self.nodes[-1] == "end"

    def possible_next_states(self):
        result = set()
        for start, end in self.maze:
            if start == self.nodes[-1]:
                if end.isupper() or end not in self.nodes:
                    result.add(MazeState(self.maze, self.nodes + [end]))
        return result



def run_part_1(data):
    start_state = MazeState(data, ["start"])
    return len(advent_tools.find_all_final_states(start_state))


class PartTwo(advent_tools.StateForGraphs):

    def __init__(self, maze, nodes):
        self.nodes = nodes
        self.maze = maze

    def __str__(self):
        return "_".join(self.nodes)

    def is_final(self):
        return self.nodes[-1] == "end"

    def possible_next_states(self):
        result = set()
        for start, end in self.maze:
            if start == self.nodes[-1]:
                if self.valid_state(end):
                    result.add(PartTwo(self.maze, self.nodes + [end]))
        return result

    def valid_state(self, next_node):
        if next_node.isupper():
            return True
        if next_node == "start":
            return False
        if next_node == "end" and "end" in self.nodes:
            return False
        lower_counts = collections.Counter([n for n in self.nodes if n.islower()])
        count_counts = collections.Counter(lower_counts.values())
        if count_counts[2] == 1:
            if next_node in self.nodes:
                return False
        return True


def run_part_2(data):
    start_state = PartTwo(data, ["start"])
    return len(advent_tools.find_all_final_states(start_state))


if __name__ == '__main__':
    main()