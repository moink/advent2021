import itertools
from functools import partial

import advent_tools


def main():
    data = advent_tools.read_input_lines()
    data = process_input(data)
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def process_input(data):
    result = []
    for line in data:
        result.append(eval(line))
    return result


def add_to_result(result, nesting, to_add):
    p = result
    for level in nesting[:-1]:
        p = p[level]
    p[nesting[-1]] += to_add


def create_add_fun(result, nesting_level):
    nesting1 = [len(result) - 1]
    p = result
    for level in range(1, nesting_level + 1):
        nesting1.append(len(p[-1]) - 1)
        p = p[-1]
    nesting = nesting1
    return partial(add_to_result, nesting=nesting)


def do_nothing(result, to_add):
    pass


def append_to_result(result, level, to_append):
    p = result
    for lev in range(level):
        p = p[-1]
    p.append(to_append)


def try_explode(pair0):
    result = []
    right = 0
    have_exploded = False
    add_fun = do_nothing
    all_pairs = iterate_list(pair0, 0)
    _, _ = next(all_pairs)
    level, pair = next(all_pairs)
    while pair is not None:
        if isinstance(pair, list):
            if level == 4:
                if not have_exploded:
                    _, left = next(all_pairs)
                    _, right = next(all_pairs)
                    add_fun(result=result, to_add=left)
                    append_to_result(result, 3, 0)
                    have_exploded = True
                else:
                    _, left2 = next(all_pairs)
                    _, right2 = next(all_pairs)
                    append_to_result(result, 3, [left2 + right, right2])
                    right = 0
            else:
                append_to_result(result, level - 1, [])
        else:
            append_to_result(result, level - 1, pair + right)
            add_fun = create_add_fun(result, level - 1)
            right = 0
        level, pair = next(all_pairs, (None, None))
    return result


def iterate_list(pair0, level):
    yield level, pair0
    if isinstance(pair0, list):
        for elem in pair0:
            yield from iterate_list(elem, level + 1)


def try_split(line):
    if isinstance(line, int):
        if line >= 10:
            left = line // 2
            right = line - left
            return [left, right], True
        return line, False
    have_split = False
    result = []
    for child in line:
        if not have_split:
            new_child, have_split = try_split(child)
        else:
            new_child = child
        result.append(new_child)
    return result, have_split


def run_part_1(data):
    return calc_magnitude(sum_snailfish(data))


def sum_snailfish(data):
    result = reduce_snailfish(data[0])
    for line in data[1:]:
        result = reduce_snailfish([result, line])
    return result


def reduce_snailfish(line):
    finished = False
    while not finished:
        line, finished = try_next_step(line)
    return line


def try_next_step(line):
    new_line = try_explode(line)
    if new_line != line:
        return new_line, False
    new_line, _ = try_split(line)
    if new_line != line:
        return new_line, False
    return line, True


def calc_magnitude(expr):
    if isinstance(expr, int):
        return expr
    return 3 * calc_magnitude(expr[0]) + 2 * calc_magnitude(expr[1])


def run_part_2(data):
    return max(calc_magnitude(sum_snailfish(p))
               for p in itertools.permutations(data, 2))


if __name__ == '__main__':
    main()