from functools import reduce
from operator import mul

import advent_tools


def main():
    data = advent_tools.read_whole_input()
    data, _ = process_input(data)
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def process_input(hex):
    bits = bin(int(hex, 16))[2:]
    len_data = len(bits)
    if len_data % 4 > 0:
        bits = "0" * (4 - len_data % 4) + bits
    return make_packet_tree(bits)


def get_version_sum(packet_tree):
    return (
        packet_tree["version"]
        + sum(get_version_sum(child) for child in packet_tree["children"])
    )


def run_part_1(packet_tree):
    return get_version_sum(packet_tree)


def make_packet_tree(bits):
    result = {
        "version": int(bits[0:3], 2),
        "type_id": int(bits[3:6], 2),
        "children": []
    }
    if result["type_id"] == 4:
        result["value"], rest = read_literal_value(bits[6:])
        return result, rest
    else:
        length_type_id = bits[6]
        if length_type_id == "0":
            length_of_subpackets = int(bits[7:22], 2)
            sub_rest = bits[22:22+length_of_subpackets]
            rest = bits[22+length_of_subpackets:]
            while len(sub_rest) > 0:
                value, sub_rest = make_packet_tree(sub_rest)
                result["children"].append(value)
        else:
            number_of_subpackets = int(bits[7:18], 2)
            rest = bits[18:]
            for _ in range(number_of_subpackets):
                subpacket, rest = make_packet_tree(rest)
                result["children"].append(subpacket)
        return result, rest


def read_literal_value(bits):
    rest = bits
    not_last = "1"
    binary_num = ""
    while not_last != "0":
        not_last, this_chunk, rest = rest[0], rest[1:5], rest[5:]
        binary_num = binary_num + this_chunk
    return int(binary_num, 2), rest


def run_part_2(packet_tree):
    return get_value(packet_tree)


def get_value(packet_tree):
    type_id = packet_tree["type_id"]
    if type_id == 4:
        return packet_tree["value"]
    if type_id == 0:
        return sum(get_value(child) for child in packet_tree["children"])
    if type_id == 1:
        return reduce(mul, (get_value(child) for child in packet_tree["children"]), 1)
    if type_id == 2:
        return min(get_value(child) for child in packet_tree["children"])
    if type_id == 3:
        return max(get_value(child) for child in packet_tree["children"])
    if type_id == 5:
        return int(get_value(packet_tree["children"][0])
                   > get_value(packet_tree["children"][1]))
    if type_id == 6:
        return int(get_value(packet_tree["children"][0])
                   < get_value(packet_tree["children"][1]))
    if type_id == 7:
        return int(get_value(packet_tree["children"][0])
                   == get_value(packet_tree["children"][1]))
    raise RuntimeError(f"Invalid type id {type_id}")


if __name__ == '__main__':
    main()