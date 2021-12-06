import collections

import advent_tools


def main():
    data = advent_tools.read_all_integers()[0]
    print('Part 1:', run_simulation(data, 80))
    print('Part 2:', run_simulation(data, 256))


def run_simulation(data, n_steps):
    counts = collections.Counter(data)
    for _ in range(n_steps):
        zero_count = counts.pop(0, 0)
        new_counts = collections.defaultdict(int, {n - 1: c for n, c in counts.items()})
        new_counts[6] = new_counts[6] + zero_count
        new_counts[8] = zero_count
        counts = new_counts
    return sum(counts.values())


if __name__ == '__main__':
    main()