import advent_tools


def main():
    data = advent_tools.read_input_lines()
    data = process_input(data)
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def process_input(data):
    result = []
    for line in data:
        direction, str_step = line.split()
        step = int(str_step)
        result.append((direction, step))
    return result

def run_part_1(data):
    depth = 0
    pos = 0
    for direction, step in data:
        if direction == "forward":
            pos = pos + step
        elif direction == "up":
            depth = depth - step
        elif direction == "down":
            depth = depth + step
        else:
            raise RuntimeError(f"Unknown direction '{direction}'")
    return depth * pos


def run_part_2(data):
    depth = 0
    pos = 0
    aim = 0
    for direction, step in data:
        if direction == "forward":
            pos = pos + step
            depth = depth + aim * step
        elif direction == "up":
            aim = aim - step
        elif direction == "down":
            aim = aim + step
        else:
            raise RuntimeError(f"Unknown direction '{direction}'")
    return depth * pos


if __name__ == '__main__':
    main()