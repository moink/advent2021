import collections
import itertools
import time

import pandas as pd
from matplotlib import pyplot as plt

import advent_tools

MIN_SCORE_TO_WIN = 21


def main():
    data = advent_tools.read_all_integers()
    p1start = data[0][1]
    p2start = data[1][1]
    print('Part 1:', run_part_1(p1start, p2start))
    start_time = time.perf_counter()
    part2 = run_part_2(p1start, p2start)
    print('Part 2:', part2)
    elapsed = time.perf_counter() - start_time
    print("Elapsed time:", elapsed)



def get_roll(roll_num, player_num):
    a = 9 * player_num - 3
    return 18 * roll_num + a


def get_points(roll_num, player_num, start):
    s = sum(get_roll(i, player_num) for i in range(roll_num + 1)) + start
    return (s - 1) % 10 + 1


def run_part_1(start1, start2):
    points1 = {i: get_points(i, 1, start1) for i in range(10)}
    points2 = {i: get_points(i, 2, start2) for i in range(10)}
    ten_roll_points1 = sum(points1.values())
    ten_roll_points2 = sum(points2.values())
    rolls = 10 * min(1000 // ten_roll_points1, 1000 // ten_roll_points2)
    sum1 = rolls // 10 * ten_roll_points1
    sum2 = rolls // 10 * ten_roll_points2
    rolls1 = rolls2 = rolls - 1
    while sum1 < 1000 and sum2 < 1000:
        rolls1 += 1
        sum1 += points1[rolls1 % 10]
        if sum1 < 1000:
            rolls2 += 1
            sum2 += points2[rolls2 % 10]
    return 3 * min(sum1, sum2) * (rolls1 + rolls2 + 2)


def run_part_2(start1, start2):
    counts = collections.Counter(
        sum(rolls) for rolls in itertools.product(range(1, 4), repeat=3)
    )
    state_counts = {(start1, 0, start2, 0): 1}
    win1 = 0
    win2 = 0
    while state_counts:
        new_states = collections.defaultdict(int)
        for roll_sum, roll_count in counts.items():
            for (p1_spot, p1_points, p2_spot, p2_points), count in state_counts.items():
                p1_spot = (p1_spot + roll_sum - 1) % 10 + 1
                p1_points += p1_spot
                if p1_points >= MIN_SCORE_TO_WIN:
                    win1 += count * roll_count
                else:
                    state = (p1_spot, p1_points, p2_spot, p2_points)
                    new_states[state] += count * roll_count
        state_counts = {**new_states}
        new_states = collections.defaultdict(int)
        for p2_roll_sum, p2_count in counts.items():
            for (p1_spot, p1_points, p2_spot, p2_points), count in state_counts.items():
                p2_spot = (p2_spot + p2_roll_sum - 1) % 10 + 1
                p2_points += p2_spot
                if p2_points >= MIN_SCORE_TO_WIN:
                    win2 += count * p2_count
                else:
                    state = (p1_spot, p1_points, p2_spot, p2_points)
                    new_states[state] += count * p2_count
        state_counts = {**new_states}
    return max(win1, win2)


if __name__ == '__main__':
    main()
