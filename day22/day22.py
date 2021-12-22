import functools
import itertools

import numpy as np
from matplotlib import pyplot as plt

import advent_tools


def main():
    ints = advent_tools.read_all_integers()
    lines = advent_tools.read_input_lines()
    instructions = process_input(ints, lines)
    print('Part 1:', run_program(instructions, True))
    print('Part 2:', run_program(instructions, False))


def process_input(data, lines):
    result = []
    for coordinates, l in zip(data, lines):
        try:
            x1, x2, y1, y2, z1, z2 = coordinates
        except ValueError:
            print("Value error", coordinates)
        else:
            if l.startswith("on"):
                result.append((True, (x1, x2+1, y1, y2+1, z1, z2+1)))
            else:
                result.append((False, (x1, x2+1, y1, y2+1, z1, z2+1)))
    return result


def run_program(data, limit_area):
    grid = set()
    for state, coordinates in data:
        if not limit_area or (min(coordinates) >= -50 and max(coordinates) <= 51):
            if state:
                grid = add_to_all(grid, RectangularPrism(*coordinates))
            else:
                grid = subtract_from_all(grid, RectangularPrism(*coordinates))
    return sum(prism.volume() for prism in grid)


def add_to_all(current_state, new_prism):
    result = subtract_from_all(current_state, new_prism)
    result.add(new_prism)
    return result


def subtract_from_all(current_state, new_prism):
    result = set()
    for prism in current_state:
        differences = prism - new_prism
        result = result.union(differences)
    return result


@functools.total_ordering
class RectangularPrism:

    def __init__(self, x_min, x_max, y_min, y_max, z_min, z_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.z_min = z_min
        self.z_max = z_max

    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):
        return str(self) < str(other)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return (f"RectangularPrism("
                f"{self.x_min}, {self.x_max},"
                f" {self.y_min}, {self.y_max},"
                f" {self.z_min}, {self.z_max})")

    def __contains__(self, item):
        x, y, z = item
        return (
            self.x_min < x < self.x_max
            and self.y_min < y < self.y_max
            and self.z_min < z < self.z_max
        )

    def __sub__(self, other):
        if self.am_completely_inside(other):
            return set()
        if self.no_intersection_with(other):
            return {self}
        x_ranges = self.get_axis_ranges(
            self.x_min, self.x_max, other.x_min, other.x_max
        )
        y_ranges = self.get_axis_ranges(
            self.y_min, self.y_max, other.y_min, other.y_max
        )
        z_ranges = self.get_axis_ranges(
            self.z_min, self.z_max, other.z_min, other.z_max
        )
        result = set()
        for x_range, y_range, z_range in itertools.product(
                x_ranges, y_ranges, z_ranges
        ):
            if (
                self.contains_range(x_range, y_range, z_range)
                and not other.contains_range(x_range, y_range, z_range)
            ):
                result.add(RectangularPrism(
                    x_range[0], x_range[1],
                    y_range[0], y_range[1],
                    z_range[0], z_range[1]
                ))
        return result

    def no_intersection_with(self, other):
        return (
            self.x_max <= other.x_min or self.x_min >= other.x_max
            or self.y_max <= other.y_min or self.y_min >= other.y_max
            or self.z_max <= other.z_min or self.z_min >= other.z_max
        )

    def am_completely_inside(self, other):
        return (
            other.x_min < self.x_min and other.x_max > self.x_max
            and other.y_min < self.y_min and other.y_max > self.y_max
            and other.z_min < self.z_min and other.z_max > self.z_max
        )

    def get_axis_ranges(self, self_min, self_max, other_min, other_max):
        return [
            (range_min, range_max) for (range_min, range_max)
            in self.get_unfiltered_axis_ranges(self_min, self_max, other_min, other_max)
            if range_max > range_min
        ]

    @staticmethod
    def get_unfiltered_axis_ranges(self_min, self_max, other_min, other_max):
        if other_min >= self_max or self_min >= other_max:
            return [(self_min, self_max)]
        if self_min <= other_min <= self_max <= other_max:
            return [(self_min, other_min), (other_min, self_max)]
        if self_min <= other_min <= other_max <= self_max:
            return [(self_min, other_min), (other_min, other_max), (other_max, self_max)]
        if other_min <= self_min and self_max <= other_max:
            return [(self_min, self_max)]
        if other_min <= self_min <= other_max <= self_max:
            return [(other_min, self_min), (self_min, other_max), (other_max, self_max)]
        raise RuntimeError("Unclear axis ordering")

    def plot(self, ax, color):
        x_range = np.array([self.x_min, self.x_max])
        y_range = np.array([self.y_min, self.y_max])
        z_range = np.array([self.z_min, self.z_max])
        xx, yy, zz0, zz1 = self.create_surface(x_range, y_range, z_range)
        self.draw_surface(ax, xx, yy, zz0, color)
        self.draw_surface(ax, xx, yy, zz1, color)
        yy, zz, xx0, xx1 = self.create_surface(y_range, z_range, x_range)
        self.draw_surface(ax, xx0, yy, zz, color)
        self.draw_surface(ax, xx1, yy, zz, color)
        xx, zz, yy0, yy1 = self.create_surface(x_range, z_range, y_range)
        self.draw_surface(ax, xx, yy0, zz, color)
        self.draw_surface(ax, xx, yy1, zz, color)

    @staticmethod
    def create_surface(x_range, y_range, z_range):
        xx, yy = np.meshgrid(x_range, y_range)
        zz0 = z_range[0] * np.ones_like(xx)
        zz1 = z_range[1] * np.ones_like(xx)
        return xx, yy, zz0, zz1

    @staticmethod
    def draw_surface(ax, xx, yy, zz, color):
        ax.plot_wireframe(xx, yy, zz, color=color)
        ax.plot_surface(xx, yy, zz, color=color, alpha=0.2)

    def volume(self):
        return (
            (self.x_max - self.x_min)
            * (self.y_max - self.y_min)
            * (self.z_max - self.z_min)
        )

    def contains_range(self, x_range, y_range, z_range):
        x = (x_range[0] + x_range[1]) / 2
        y = (y_range[0] + y_range[1]) / 2
        z = (z_range[0] + z_range[1]) / 2
        return (x, y, z) in self


def plot_grid(grid):
    plt.clf()
    ax = plt.axes(projection='3d')
    for prism in grid:
        prism.plot(ax, "r")
    plt.show()


if __name__ == '__main__':
    main()
