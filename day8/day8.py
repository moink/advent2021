from functools import partial

import advent_tools


def main():
    data = [get_rhs_digits(line) for line in advent_tools.read_input_lines()]
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def run_part_1(data):
    return sum(sum(digits.count(num) for num in ["1", "4", "7", "8"])
               for digits in data)


def run_part_2(data):
    return sum(int("".join(digits)) for digits in data)


def get_rhs_digits(line):
    left, right = line.split("|")
    not_found_yet = {"".join(sorted(word)) for word in left.split()}
    numbers_to_letters = {
        "1": get_that_matches(not_found_yet, 2),
        "4": get_that_matches(not_found_yet, 4),
        "7": get_that_matches(not_found_yet, 3),
        "8": get_that_matches(not_found_yet, 7),
    }
    numbers_to_letters["3"] = get_that_matches(
        not_found_yet, 5, partial(is_super_set, subset=numbers_to_letters["1"])
    )
    numbers_to_letters["9"] = get_that_matches(
        not_found_yet, 6, partial(is_super_set, subset=numbers_to_letters["4"])
    )
    numbers_to_letters["0"] = get_that_matches(
        not_found_yet, 6, partial(is_super_set, subset=numbers_to_letters["1"])
    )
    numbers_to_letters["6"] = get_that_matches(not_found_yet, 6)
    numbers_to_letters["5"] = get_that_matches(
        not_found_yet, 5, lambda x: is_super_set(numbers_to_letters["6"], x)
    )
    numbers_to_letters["2"] = get_that_matches(not_found_yet, 5)
    letters_to_numbers = {val: key for key, val in numbers_to_letters.items()}
    return [letters_to_numbers["".join(sorted(word))] for word in right.split()]


def get_that_matches(not_found_yet, length, fun=None):
    if fun is None:
        fun = lambda x: True
    for val in not_found_yet:
        if len(val) == length and fun(val):
            not_found_yet.remove(val)
            return val
    raise RuntimeError("No matching value")

def is_super_set(superset, subset):
    return set(subset).issubset(superset)


if __name__ == '__main__':
    main()