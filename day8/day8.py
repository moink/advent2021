import advent_tools

DIGIT_RULES = (
    # Digit, number of segments, subset digit, superset digit
    ("1", 2, None, None),
    ("4", 4, None, None),
    ("7", 3, None, None),
    ("8", 7, None, None),
    ("3", 5, "1", None),
    ("9", 6, "4", None),
    ("0", 6, "1", None),
    ("6", 6, None, None),
    ("5", 5, None, "6"),
    ("2", 5, None, None),
)


def main():
    data = [get_rhs(line) for line in advent_tools.read_input_lines()]
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def run_part_1(data):
    return sum(sum(numbers.count(digit) for digit in ["1", "4", "7", "8"])
               for numbers in data)


def run_part_2(data):
    return sum(int(numbers) for numbers in data)


def get_rhs(line):
    left, right = line.split("|")
    not_found_yet = {"".join(sorted(word)) for word in left.split()}
    numbers_to_letters = {}
    for digit, length, subset_digit, superset_digit in DIGIT_RULES:
        numbers_to_letters[digit] = get_digit(
            not_found_yet,
            length,
            numbers_to_letters.get(subset_digit, None),
            numbers_to_letters.get(superset_digit, None))
    letters_to_numbers = {val: key for key, val in numbers_to_letters.items()}
    return "".join(letters_to_numbers["".join(sorted(word))] for word in right.split())


def get_digit(not_found_yet, length, subset, superset):

    def filter_digit(candidate):
        if subset is None and superset is None:
            return len(candidate) == length
        if superset is None:
            return len(candidate) == length and set(subset).issubset(candidate)
        return len(candidate) == length and set(candidate).issubset(superset)

    for letters in not_found_yet:
        if filter_digit(letters):
            not_found_yet.remove(letters)
            return letters
    raise RuntimeError(
        f"No letters with length {length}, subset {subset} and superset {superset}"
        f" in {not_found_yet}"
    )


if __name__ == '__main__':
    main()