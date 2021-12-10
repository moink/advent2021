import collections
import statistics

import advent_tools

CLOSING_CHARS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}


def main():
    data = advent_tools.read_input_lines()
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def run_part_1(data):
    bad_chars = []
    for line in data:
        currently_in = []
        for char in line:
            if char in CLOSING_CHARS:
                currently_in.append(char)
            elif char == CLOSING_CHARS[currently_in[-1]]:
                currently_in.pop()
            else:
                bad_chars.append(char)
                break
    counts = collections.Counter(bad_chars)
    costs = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    return sum(v*costs[k] for k, v in counts.items())


def run_part_2(data):
    scores = []
    for line in data:
        completion = get_completion(line)
        if completion:
            scores.append(score_line(completion))
    return statistics.median(scores)


def get_completion(line):
    currently_in = []
    for char in line:
        if char in CLOSING_CHARS:
            currently_in.append(char)
        elif char == CLOSING_CHARS[currently_in[-1]]:
            currently_in.pop()
        elif char in CLOSING_CHARS.values():
            return ""
    else:
        completion = "".join(CLOSING_CHARS[char] for char in reversed(currently_in))
    return completion


def score_line(completion):
    char_scores = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }
    score = 0
    for char in completion:
        num = char_scores[char]
        score = 5 * score + num
    return score


if __name__ == '__main__':
    main()