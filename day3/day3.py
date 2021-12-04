import advent_tools
from advent_tools import input_filename


def main():
    with open('input.txt') as in_file:
        data = in_file.readlines()
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def run_part_1(data):
    delta_bits = []
    for pos in zip(*data):
        if pos.count("1") > pos.count("0"):
            delta_bits.append("1")
        else:
            delta_bits.append("0")
    delta = int("".join(delta_bits), 2)
    eps = ~delta & 2 ** len(data[0]) - 1
    return delta * eps


def run_part_2(data):
    ox = int(get_rating(data, 0, "1")[0], 2)
    co2 = int(get_rating(data, 0, "0")[0], 2)
    return ox * co2


def get_rating(data, pos, val_for_more_ones):
    if len(data) == 1:
        return data
    other_val = list({"0", "1"}.difference({val_for_more_ones}))[0]
    pos = pos % len(data[0])
    bits_in_pos = [line[pos] for line in data]
    if bits_in_pos.count("1") >= bits_in_pos.count("0"):
        new_data = [line for line in data if line[pos] == val_for_more_ones]
    else:
        new_data = [line for line in data if line[pos] == other_val]
    return get_rating(new_data, pos + 1, val_for_more_ones)


if __name__ == '__main__':
    main()