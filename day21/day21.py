import collections
import functools
import itertools
import time

import advent_tools

MIN_SCORE_TO_WIN = 21

ROLL_SUM_COUNTS = collections.Counter(
    sum(rolls) for rolls in itertools.product(range(1, 4), repeat=3)
)

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


def get_points(roll_num, player_num, start):
    return (sum(18 * i + 9 * player_num - 3 for i in range(roll_num + 1))
            + start) % 10 or 10


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


@functools.lru_cache(None)
def count_states(my_score, my_pos, opp_score, opp_pos):
    if opp_score >= 21:
        return 0, 1
    my_total = 0
    opp_total = 0
    for roll_sum, count in ROLL_SUM_COUNTS.items():
        new_pos = (my_pos + roll_sum) % 10 or 10
        new_score = my_score + new_pos
        opp_wins, my_wins = count_states(opp_score, opp_pos, new_score, new_pos)
        my_total += count * my_wins
        opp_total += count * opp_wins
    return my_total, opp_total


def run_part_2(p1start, p2start):
    return max(count_states(0, p1start, 0, p2start))


if __name__ == '__main__':
    main()
