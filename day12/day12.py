import collections
import time

import advent_tools


def main():
    lines = advent_tools.read_input_lines()
    maze = process_input(lines)
    print('Part 1:', run_part(PartOneMazeState, maze))
    print('Part 2:', run_part(PartTwoMazeState, maze))


def process_input(lines):
    data = []
    for line in lines:
        left, right = [word.strip() for word in line.split('-')]
        if right != "start" and left != "end":
            data.append((left, right))
        if left != "start" and right != "end":
            data.append((right, left))
    return data


class PartOneMazeState(advent_tools.StateForGraphs):

    def __init__(self, maze, nodes):
        self.nodes = nodes
        self.maze = maze

    def __str__(self):
        return ",".join(self.nodes)

    def is_final(self):
        return self.nodes[-1] == "end"

    def possible_next_states(self):
        result = set()
        for start, end in self.maze:
            if start == self.nodes[-1]:
                if self.is_valid(end):
                    result.add(self.__class__(self.maze, self.nodes + [end]))
        return result

    def is_valid(self, next_node):
        return next_node.isupper() or next_node not in self.nodes


class PartTwoMazeState(PartOneMazeState):

    def __init__(self, maze, nodes):
        super().__init__(maze, nodes)
        self.lower_twice_visited = max(collections.Counter(
            n for n in self.nodes if n.islower()).values()) > 1

    def is_valid(self, next_node):
        if next_node.isupper():
            return True
        if self.lower_twice_visited and next_node in self.nodes:
            return False
        return True


def run_part(state_class, data):
    start_state = state_class(data, ["start"])
    start = time.perf_counter()
    states = advent_tools.find_all_final_states(start_state)
    elapsed = time.perf_counter() - start
    return len(states), elapsed


if __name__ == '__main__':
    main()
