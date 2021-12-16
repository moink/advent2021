from functools import reduce
from operator import mul

import advent_tools


def main():
    hex_data = advent_tools.read_whole_input()
    bits = bits_from_hex(hex_data)
    tree, _ = make_packet_tree(bits)
    print('Part 1:', get_version_sum(tree))
    print('Part 2:', get_value(tree))


def bits_from_hex(hex_value):
    bits = bin(int(hex_value, 16))[2:]
    len_data = len(bits)
    if len_data % 4 > 0:
        bits = "0" * (4 - len_data % 4) + bits
    return bits


def make_packet_tree(bits):
    packet = {
        "version": int(bits[0:3], 2),
        "type_id": int(bits[3:6], 2),
        "children": []
    }
    if packet["type_id"] == 4:
        packet["value"], bit_remainder = read_literal_value(bits[6:])
        return packet, bit_remainder
    return make_packet_with_sub_packets(bits, packet)


def read_literal_value(bits):
    bit_remainder = bits
    not_last = True
    binary_digits = ""
    while not_last:
        not_last = bit_remainder[0] != "0"
        digit_chunk = bit_remainder[1:5]
        bit_remainder = bit_remainder[5:]
        binary_digits = binary_digits + digit_chunk
    return int(binary_digits, 2), bit_remainder


def make_packet_with_sub_packets(bits, packet):
    length_type_id = bits[6]
    if length_type_id == "0":
        length_of_sub_packets = int(bits[7:22], 2)
        sub_remainder = bits[22:22 + length_of_sub_packets]
        bit_remainder = bits[22 + length_of_sub_packets:]
        while len(sub_remainder) > 0:
            sub_packet, sub_remainder = make_packet_tree(sub_remainder)
            packet["children"].append(sub_packet)
    else:
        number_of_sub_packets = int(bits[7:18], 2)
        bit_remainder = bits[18:]
        for _ in range(number_of_sub_packets):
            sub_packet, bit_remainder = make_packet_tree(bit_remainder)
            packet["children"].append(sub_packet)
    return packet, bit_remainder


def get_version_sum(packet_tree):
    return (
        packet_tree["version"]
        + sum(get_version_sum(child) for child in packet_tree["children"])
    )


def get_value(packet_tree):
    if packet_tree["type_id"] == 0:
        return sum(get_value(child) for child in packet_tree["children"])
    if packet_tree["type_id"] == 1:
        return reduce(mul, (get_value(child) for child in packet_tree["children"]), 1)
    if packet_tree["type_id"] == 2:
        return min(get_value(child) for child in packet_tree["children"])
    if packet_tree["type_id"] == 3:
        return max(get_value(child) for child in packet_tree["children"])
    if packet_tree["type_id"] == 4:
        return packet_tree["value"]
    if packet_tree["type_id"] == 5:
        return int(get_value(packet_tree["children"][0])
                   > get_value(packet_tree["children"][1]))
    if packet_tree["type_id"] == 6:
        return int(get_value(packet_tree["children"][0])
                   < get_value(packet_tree["children"][1]))
    if packet_tree["type_id"] == 7:
        return int(get_value(packet_tree["children"][0])
                   == get_value(packet_tree["children"][1]))
    raise RuntimeError(f"Invalid type id {packet_tree['type_id']}")


if __name__ == '__main__':
    main()
