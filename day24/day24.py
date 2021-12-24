import re
import advent_tools


def main():
    relations = find_relations(*(process_input(advent_tools.read_input_lines())))
    print('Part 1:', run_part_1(relations))
    print('Part 2:', run_part_2(relations))


def process_input(data):
    added_to_x = []
    added_to_y = []
    divisors = []
    patterns_lists = [
        ((re.compile(r"add x (-?[0-9]+)")), added_to_x),
        ((re.compile(r"add y (-?[0-9]+)")), added_to_y),
        ((re.compile(r"div z (-?[0-9]+)")), divisors),
    ]
    for line in data:
        for pattern, result_list in patterns_lists:
            match = re.match(pattern, line)
            if match:
                result_list.append(int(match.group(1)))
                break
    added_to_y = added_to_y[2::3]
    return added_to_x, added_to_y, divisors


def find_relations(added_to_x, added_to_y, divisors):
    stack = []
    result = []
    for i, divisor in enumerate(divisors):
        if divisor == 1:
            stack.append(i)
        else:
            prev_num = stack.pop()
            result.append((prev_num, i, added_to_y[prev_num] + added_to_x[i]))
    return result


def run_part_1(relations):
    result = [9] * 14
    for pos1, pos2, delta in relations:
        if delta >= 0:
            result[pos1] = 9 - delta
        else:
            result[pos2] = 9 + delta
    return "".join(str(num) for num in result)


def run_part_2(relations):
    result = [1] * 14
    for pos1, pos2, delta in relations:
        if delta >= 0:
            result[pos2] = 1 + delta
        else:
            result[pos1] = 1 - delta
    return "".join(str(num) for num in result)


if __name__ == '__main__':
    main()
