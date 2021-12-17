import math

import advent_tools


def main():
    target = tuple(advent_tools.read_all_integers()[0])
    print('Part 1:', run_part_1(target[2]))
    print('Part 2:', run_part_2(target))


def run_part_1(min_y):
    return min_y * (min_y + 1) // 2


def run_part_2(target):
    min_x_vel = int(math.floor(math.sqrt(target[0])))
    max_x_vel = target[1] + 1
    max_y_vel = abs(target[1] + 1)
    min_y_vel = -max_y_vel
    return sum(hits_target(target, x_vel, y_vel)
               for x_vel in range(min_x_vel, max_x_vel)
               for y_vel in range(min_y_vel, max_y_vel))


def hits_target(target, initial_x_vel, initial_y_vel):
    target_min_x, target_max_x, target_min_y, target_max_y = target
    x_vel = initial_x_vel
    y_vel = initial_y_vel
    x_pos = 0
    y_pos = 0
    while y_pos > target_min_y and x_pos < target_max_x:
        x_pos += x_vel
        y_pos += y_vel
        x_vel = max(0, x_vel - 1)
        y_vel -= 1
        if (target_min_x <= x_pos <= target_max_x
                and target_min_y <= y_pos <= target_max_y):
            return True
    return False


if __name__ == '__main__':
    main()
