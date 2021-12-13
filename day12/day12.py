import collections
import time

import advent_tools

MAZE = {}


def process_input(lines):
    edges = collections.defaultdict(list)
    for line in lines:
        left, right = line.split('-')
        if right != "start" and left != "end":
            edges[left].append(right)
        if left != "start" and right != "end":
            edges[right].append(left)
    return dict(edges)


class PartOneMazeState(advent_tools.StateForGraphs):

    def __init__(self, nodes):
        self.nodes = nodes

    def __str__(self):
        return ",".join(self.nodes)

    def is_final(self):
        return self.nodes[-1] == "end"

    def possible_next_states(self):
        return {self.__class__(self.nodes + [next_node])
                for next_node in MAZE[self.nodes[-1]]
                if self.is_valid(next_node)}

    def is_valid(self, next_node):
        return next_node.isupper() or next_node not in self.nodes


class PartTwoMazeState(PartOneMazeState):

    def __init__(self, nodes):
        super().__init__(nodes)
        self.lower_twice_visited = max(collections.Counter(
            n for n in self.nodes if n.islower()).values()) > 1

    def is_valid(self, next_node):
        return (next_node.isupper() or not self.lower_twice_visited
                or next_node not in self.nodes)


def run_part(state_class):
    start_state = state_class(["start"])
    start = time.perf_counter()
    states = advent_tools.find_all_final_states(start_state)
    elapsed = time.perf_counter() - start
    return len(states), elapsed


if __name__ == '__main__':
    MAZE = process_input(advent_tools.read_input_lines())
    print('Part 1:', run_part(PartOneMazeState))
    print('Part 2:', run_part(PartTwoMazeState))
