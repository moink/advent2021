import math


RIGHT_ANSWER = {(23, -10), (25, -9), (27, -5), (29, -6), (22, -6), (21, -7), (9, 0), (), (27, -7), (24, -5),
     (25, -7), (26, -6), (25, -5), (6, 8), (), (11, -2), (20, -5), (29, -10), (6, 3), (), (28, -7),
     (8, 0), (), (30, -6), (29, -8), (20, -10), (6, 7), (), (6, 4), (), (6, 1), (), (14, -4), (21, -6),
     (26, -10), (7, -1), (), (7, 7), (), (8, -1), (), (21, -9), (6, 2), (), (20, -7), (30, -10), (14, -3),
     (20, -8), (13, -2), (7, 3), (), (28, -8), (29, -9), (15, -3), (22, -5), (26, -8), (25, -8),
     (25, -6), (15, -4), (9, -2), (), (15, -2), (12, -2), (28, -9), (12, -3), (24, -6), (23, -7),
     (25, -10), (7, 8), (), (11, -3), (26, -7), (7, 1), (), (23, -9), (6, 0), (), (22, -10), (27, -6),
     (8, 1), (), (22, -8), (13, -4), (7, 6), (), (28, -6), (11, -4), (12, -4), (26, -9), (7, 4),
     (24, -10), (23, -8), (30, -8), (7, 0), (), (9, -1), (), (10, -1), (26, -5), (22, -9), (6, 5),
     (7, 5), (), (23, -6), (28, -10), (10, -2), (11, -1), (20, -9), (14, -2), (29, -7), (13, -3),
     (23, -5), (24, -8), (27, -9), (30, -7), (28, -5), (21, -10), (7, 9), (), (6, 6), (), (21, -5),
     (27, -10), (7, 2), (), (30, -9), (21, -8), (22, -7), (24, -9), (20, -6), (6, 9), (), (29, -5),
     (8, -2), (), (27, -8), (30, -5), (24, -7)}


def main():
    print('Part 2:', run_part_2())



def run_part_1():
    # target area: x=217..240, y=-126..-69
    x_pos = 0
    y_pos = 0
    best_y_vel = 0
    max_height = 0
    for initial_y_vel in range(100, 1000):
        for initial_x_vel in range(0, 1000):
            height = get_if_passes_through(initial_x_vel, initial_y_vel, x_pos, y_pos)
            if height >= max_height:
                max_height = height
                best_y_vel = initial_y_vel
    return best_y_vel, max_height


def get_if_passes_through(initial_x_vel, initial_y_vel, x_pos, y_pos):
    target_min_x = 20
    target_max_x = 30
    target_min_y = -10
    target_max_y = -5
    # target_min_x = 217
    # target_max_x = 240
    # target_min_y = -126
    # target_max_y = -69
    x_vel = initial_x_vel
    y_vel = initial_y_vel
    max_y_pos = 0
    while y_pos > target_min_y and x_pos < target_max_x:
        x_pos = x_pos + x_vel
        y_pos = y_pos + y_vel
        x_vel = max(0, x_vel - 1)
        y_vel = y_vel - 1
        if y_pos > max_y_pos:
            max_y_pos = y_pos
        if target_min_x <= x_pos <= target_max_x and target_min_y <= y_pos <= target_max_y:
            return max_y_pos
    return None


def run_part_2():
    x_pos = 0
    y_pos = 0
    count = 0
    good_vals = set()
    # return get_if_passes_through2(7, 7)
    for initial_x_vel in range(0, 1600):
        for initial_y_vel in range(-800, 800):
            height = get_if_passes_through2(initial_x_vel, initial_y_vel)
            if height:
                good_vals.add((initial_x_vel, initial_y_vel))
        if initial_x_vel % 100 == 0:
            print(len(good_vals))
    return len(good_vals)

def get_if_passes_through2(initial_x_vel, initial_y_vel):
    target_min_x = 20
    target_max_x = 30
    target_min_y = -10
    target_max_y = -5
    target_min_x = 217
    target_max_x = 240
    target_min_y = -126
    target_max_y = -69
    x_vel = initial_x_vel
    y_vel = initial_y_vel
    x_pos = 0
    y_pos = 0
    while y_pos > target_min_y and x_pos < target_max_x:
        x_pos = x_pos + x_vel
        y_pos = y_pos + y_vel
        x_vel = max(0, x_vel - 1)
        y_vel = y_vel - 1
        if target_min_x <= x_pos <= target_max_x and target_min_y <= y_pos <= target_max_y:
            return True
    return False

if __name__ == '__main__':
    main()