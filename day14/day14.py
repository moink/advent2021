import collections

import advent_tools


def main():
    (polymer, *_), map_part = advent_tools.read_input_line_groups()
    insertion_map = read_insertion_map(map_part)
    print('Part 1:', run_part(polymer, insertion_map, 10))
    print('Part 2:', run_part(polymer, insertion_map, 40))


def read_insertion_map(map_part):
    insertion_map = {}
    for line in map_part:
        left, right = line.split(' -> ')
        insertion_map[left.strip()] = right.strip()
    return insertion_map


def run_part(polymer, insertion_map, steps):
    pair_counts = collections.defaultdict(int)
    char_counts = collections.defaultdict(int, collections.Counter(polymer))
    for first_char, second_char in zip(polymer[:-1], polymer[1:]):
        pair_counts["".join((first_char, second_char))] += 1
    for _ in range(steps):
        new_pair_counts = collections.defaultdict(int)
        for pair, count in pair_counts.items():
            first_char, second_char = pair
            between = insertion_map[pair]
            new_pair_counts["".join((first_char, between))] += count
            new_pair_counts["".join((between, second_char))] += count
            char_counts[between] += count
        pair_counts = new_pair_counts
    return max(char_counts.values()) - min(char_counts.values())

if __name__ == '__main__':
    main()