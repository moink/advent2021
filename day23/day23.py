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

ALLOWED_HALLWAY_PAUSING_SPOTS = [0, 1, 3, 5, 7, 9, 10]

EMPTY_HALLWAY = ["."] * 11

TESTING_START_ROOMS = ["BA", "CD", "BC", "DA"]

DESTINATION_ROOMS = {"A": 0, "B": 1, "C":2, "D":3}

STEP_COSTS = {"A": 1, "B": 10, "C": 100, "D": 1000}

def main():
    print('Part 1:', run_part_1(["AD", "CD", "BB", "AC"]))
    print('Part 2:', run_part_2(["ADDD", "CCBD", "BBAB", "AACC"]))


def process_input(data):
    print(data)
    return data


class AmphiState(advent_tools.StateForGraphs):

    def __init__(self, hallway, rooms):
        self.hallway = [char for char in hallway]
        self.rooms = [[char for char in room] for room in rooms]

    def __str__(self):
        return "_".join(["".join(self.hallway), ":".join(("".join(room) for room in self.rooms))])

    def __repr__(self):
        return str(self)

    def is_final(self):
        return self.rooms == [["A", "A"], ["B", "B"], ["C", "C"], ["D", "D"]]

    def possible_next_states(self):
        heuristic_order = [
            self.move_down_in_rooms,
            self.move_up_in_rooms,
            self.hallway_to_room_moves,
            self.room_to_room_moves,
            self.room_to_hallway_moves
        ]
        for heuristic in heuristic_order:
            states = heuristic()
            if states:
                return states
        return set()

    def move_down_in_rooms(self):
        all_states = set()
        for room_num, room in enumerate(self.rooms):
            moving_amphi = room[0]
            if (is_empty(room[1]) and not is_empty(moving_amphi)
                    and DESTINATION_ROOMS[moving_amphi] == room_num):
                new_hallway, new_rooms = self.copy_hallway_and_rooms()
                new_rooms[room_num] = [".", moving_amphi]
                return {(
                    self.__class__(new_hallway, new_rooms),
                    STEP_COSTS[moving_amphi])}
        return all_states

    def move_up_in_rooms(self):
        all_states = set()
        for room_num, room in enumerate(self.rooms):
            if not(is_empty(room[1])):
                moving_amphi = room[1]
                if is_empty(room[0]) and room_num != DESTINATION_ROOMS[moving_amphi]:
                    new_hallway, new_rooms = self.copy_hallway_and_rooms()
                    new_rooms[room_num] = [moving_amphi, "."]
                    return {(
                        self.__class__(new_hallway, new_rooms),
                        STEP_COSTS[moving_amphi])}
        return all_states

    def room_to_hallway_moves(self):
        all_states = set()
        for room_num, leaving_room in enumerate(self.rooms):
            moving_amphi = leaving_room[0]
            if not is_empty(moving_amphi):
                for destination_spot in ALLOWED_HALLWAY_PAUSING_SPOTS:
                    if self.hallway_empty_between(space_above_room(room_num), destination_spot):
                        new_hallway, new_rooms = self.copy_hallway_and_rooms()
                        new_hallway[destination_spot] = moving_amphi
                        new_rooms[room_num][0] = "."
                        steps = 1 + abs(destination_spot - space_above_room(room_num))
                        all_states.add(
                            (self.__class__(new_hallway, new_rooms),
                                       STEP_COSTS[moving_amphi] * steps)
                        )
        return all_states

    def hallway_to_room_moves(self):
        all_states = set()
        for hallway_pos, moving_amphi in enumerate(self.hallway):
            if not is_empty(moving_amphi):
                room_num = DESTINATION_ROOMS[moving_amphi]
                arriving_room = self.rooms[room_num]
                if (
                    is_empty(arriving_room[0])
                    and (self.hallway_empty_between(
                    hallway_pos + 1,
                    space_above_room(room_num))
                    or self.hallway_empty_between(
                    hallway_pos - 1,
                    space_above_room(room_num)))
                    and(is_empty(arriving_room[1]) or arriving_room[1] == moving_amphi)
                ):
                    new_hallway, new_rooms = self.copy_hallway_and_rooms()
                    new_hallway[hallway_pos] = "."
                    new_rooms[room_num][0] = moving_amphi
                    steps = 1 + abs(hallway_pos - space_above_room(room_num))
                    all_states.add(
                        (self.__class__(new_hallway, new_rooms),
                                   STEP_COSTS[moving_amphi] * steps)
                    )
        return all_states

    def room_to_room_moves(self):
        all_states = set()
        for leaving_room_num, leaving_room in enumerate(self.rooms):
            moving_amphi = leaving_room[0]
            if not is_empty(moving_amphi):
                arriving_room_num = DESTINATION_ROOMS[moving_amphi]
                arriving_room = self.rooms[arriving_room_num]
                if (
                    is_empty(arriving_room[0])
                    and self.hallway_empty_between(
                        space_above_room(leaving_room_num),
                        space_above_room(arriving_room_num))):
                    new_hallway, new_rooms = self.copy_hallway_and_rooms()
                    new_rooms[leaving_room_num][0] = "."
                    new_rooms[arriving_room_num][0] = moving_amphi
                    steps = 2 + abs(space_above_room(arriving_room_num) - space_above_room(leaving_room_num))
                    all_states.add(
                        (self.__class__(new_hallway, new_rooms),
                                    STEP_COSTS[moving_amphi] * steps)
                    )
        return all_states

    def copy_hallway_and_rooms(self):
        new_hallway = copy.copy(self.hallway)
        new_rooms = copy.deepcopy(self.rooms)
        return new_hallway, new_rooms

    def hallway_empty_between(self, start_pos, end_pos):
        if start_pos == end_pos:
            return True
        a = min(start_pos, end_pos)
        b = max(start_pos, end_pos) + 1
        return is_empty(self.hallway[a:b])



class AmphiState2(AmphiState):

    def is_final(self):
        final = self.rooms == [["A", "A", "A", "A"], ["B", "B", "B", "B"],
                               ["C", "C", "C", "C"], ["D", "D", "D", "D"]]
        return final

    def move_down_in_rooms(self):
        all_states = set()
        for room_num, room in enumerate(self.rooms):
            for pos in range(3):
                moving_amphi = room[pos]
                if (is_empty(room[pos + 1]) and not is_empty(moving_amphi)
                        and DESTINATION_ROOMS[moving_amphi] == room_num
                        and all(char in [moving_amphi, "."] for char in room[pos:])):
                    new_hallway, new_rooms = self.copy_hallway_and_rooms()
                    new_rooms[room_num][pos] = "."
                    new_rooms[room_num][pos + 1] = moving_amphi
                    all_states.add((
                        self.__class__(new_hallway, new_rooms),
                        STEP_COSTS[moving_amphi]))
        return all_states

    def move_up_in_rooms(self):
        all_states = set()
        for room_num, room in enumerate(self.rooms):
            for pos in range(1, 4):
                if not(is_empty(room[pos])):
                    moving_amphi = room[pos]
                    if (
                        is_empty(room[pos - 1])
                        and (
                            room_num != DESTINATION_ROOMS[moving_amphi]
                            or not all(char in [moving_amphi, "."] for char in room[pos:])
                        )
                    ):
                        new_hallway, new_rooms = self.copy_hallway_and_rooms()
                        new_rooms[room_num][pos] = "."
                        new_rooms[room_num][pos - 1] = moving_amphi
                        all_states.add((
                            self.__class__(new_hallway, new_rooms),
                            STEP_COSTS[moving_amphi]))
        return all_states


def is_empty(location):
    if len(location) == 1:
        return location == "."
    return all(is_empty(char) for char in location)


def space_above_room(room_num):
    return 2 * (room_num + 1)


def move_pos_in_room(room, moving_amphi, start, end):
    result_chars = []
    for i, char in enumerate(room):
        if i == start:
            result_chars.append(".")
        elif i == end:
            result_chars.append(moving_amphi)
        else:
            result_chars.append(char)
    return ".".join(result_chars)


def run_part_1(rooms):
    first_state = AmphiState(EMPTY_HALLWAY, rooms)
    return advent_tools.bfs_min_cost_path(first_state)


def run_part_2(rooms):
    first_state = AmphiState2(EMPTY_HALLWAY, rooms)
    return advent_tools.bfs_min_cost_path(first_state)


if __name__ == '__main__':
    main()
