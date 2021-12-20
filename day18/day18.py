import itertools
from functools import partial

import advent_tools


def main():
    data = advent_tools.read_input_lines()
    snailfish_numbers = process_input(data)
    print('Part 1:', run_part_1(snailfish_numbers))
    print('Part 2:', run_part_2(snailfish_numbers))


def process_input(data):
    snailfish_numbers = []
    for line in data:
        snailfish_numbers.append(eval(line))
    return snailfish_numbers


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


def try_explode(root):
    result = []
    stored_value = 0
    have_exploded = False
    add_fun = do_nothing
    all_pairs = iterate_list(root, -1)
    _, _ = next(all_pairs)
    level, pair = next(all_pairs)
    while pair is not None:
        if isinstance(pair, int):
            append_to_result(result, level, pair + stored_value)
            add_fun = create_add_fun(result, level)
            stored_value = 0
        elif level == 3:
            _, left = next(all_pairs)
            _, right = next(all_pairs)
            if not have_exploded:
                add_fun(result=result, to_add=left)
                append_to_result(result, 3, 0)
                stored_value = right
                have_exploded = True
            else:
                append_to_result(result, 3, [left + stored_value, right])
                stored_value = 0
        else:
            append_to_result(result, level, [])
        level, pair = next(all_pairs, (None, None))
    return result


def do_nothing(result, to_add):
    pass


def iterate_list(pair0, level):
    yield level, pair0
    if isinstance(pair0, list):
        for elem in pair0:
            yield from iterate_list(elem, level + 1)


def append_to_result(result, level, to_append):
    get_nested_list_at_level(result, [-1] * level).append(to_append)


def get_nested_list_at_level(result, nesting):
    this_level_list = result
    for level in nesting:
        this_level_list = this_level_list[level]
    return this_level_list


def create_add_fun(result, nesting_level):
    nesting = [len(result) - 1]
    this_level_list = result
    for level in range(1, nesting_level + 1):
        nesting.append(len(this_level_list[-1]) - 1)
        this_level_list = this_level_list[-1]
    return partial(add_to_result, nesting=nesting)


def add_to_result(result, nesting, to_add):
    get_nested_list_at_level(result, nesting[:-1])[nesting[-1]] += to_add


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


def calc_magnitude(expr):
    if isinstance(expr, int):
        return expr
    return 3 * calc_magnitude(expr[0]) + 2 * calc_magnitude(expr[1])


def run_part_2(data):
    return max(calc_magnitude(sum_snailfish(p))
               for p in itertools.permutations(data, 2))


if __name__ == '__main__':
    main()
