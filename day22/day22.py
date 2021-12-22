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
    for state, coords in data:
        if not limit_area or (min(coords) >= -50 and max(coords) <= 51):
            if state:
                grid = add_to_all(grid, RectangularPrism(*coords))
            else:
                grid = subtract_from_all(grid, RectangularPrism(*coords))
    return sum(prism.volume() for prism in grid)


def plot_grid(grid):
    plt.clf()
    ax = plt.axes(projection='3d')
    for prism in grid:
        prism.plot(ax, "r")
    plt.show()


def mid_point_in(x_range, y_range, z_range, prism):
    x = (x_range[0] + x_range[1])/2
    y = (y_range[0] + y_range[1])/2
    z = (z_range[0] + z_range[1])/2
    return (x, y, z)  in prism

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
        return (
            self.x_min == other.x_min and self.x_max == other.x_max and
            self.y_min == other.y_min and self.y_max == other.y_max and
            self.z_min == other.z_min and self.z_max == other.z_max
        )

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

    def iter_points(self):
        for x in range(self.x_min, self.x_max):
            for y in range(self.y_min, self.y_max):
                for z in range(self.z_min, self.z_max):
                    yield x, y, z

    def __contains__(self, item):
        x, y, z = item
        return (
                self.x_min < x < self.x_max
                and self.y_min < y < self.y_max
                and self.z_min < z < self.z_max
        )

    def __sub__(self, other):
        if (
                other.x_min < self.x_min and other.x_max > self.x_max
                and other.y_min < self.y_min and other.y_max > self.y_max
                and other.z_min < self.z_min and other.z_max > self.z_max
        ):
            return set()
        if (
            self.x_max <= other.x_min or self.x_min >= other.x_max
            or self.y_max <= other.y_min or self.y_min >= other.y_max
            or self.z_max <= other.z_min or self.z_min >= other.z_max
        ):
            return {self}
        x_ranges = self.get_axis_ranges(self.x_min, self.x_max, other.x_min, other.x_max)
        y_ranges = self.get_axis_ranges(self.y_min, self.y_max, other.y_min, other.y_max)
        z_ranges = self.get_axis_ranges(self.z_min, self.z_max, other.z_min, other.z_max)
        result = set()
        for x_range, y_range, z_range in itertools.product(x_ranges, y_ranges, z_ranges):
            if (
                x_range[1] > x_range[0]
                and y_range[1] > y_range[0]
                and z_range[1] > z_range[0]
                and mid_point_in(x_range, y_range, z_range, self)
                and not mid_point_in(x_range, y_range, z_range, other)
            ):
                result.add(RectangularPrism(
                    x_range[0], x_range[1],
                    y_range[0], y_range[1],
                    z_range[0], z_range[1]
                ))
        assert(not [(p1, p2) for p1, p2 in itertools.product(result, repeat=2)
                    if (p1 - p2) != {p1} and p1 != p2])
        return result

    def get_axis_ranges(self, self_min, self_max, other_min, other_max):
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
        xx, yy = np.meshgrid(x_range, y_range)
        zz = z_range[0] * np.ones_like(xx)
        ax.plot_wireframe(xx, yy, zz, color=color)
        ax.plot_surface(xx, yy, zz, color=color, alpha=0.2)
        zz = z_range[1] * np.ones_like(xx)
        ax.plot_wireframe(xx, yy, zz, color=color)
        ax.plot_surface(xx, yy, zz, color=color, alpha=0.2)
        yy, zz = np.meshgrid(y_range, z_range)
        xx = x_range[0] * np.ones_like(yy)
        ax.plot_wireframe(xx, yy, zz, color=color)
        ax.plot_surface(xx, yy, zz, color=color, alpha=0.2)
        xx = x_range[1] * np.ones_like(yy)
        ax.plot_wireframe(xx, yy, zz, color=color)
        ax.plot_surface(xx, yy, zz, color=color, alpha=0.2)
        xx, zz = np.meshgrid(x_range, z_range)
        yy = y_range[0] * np.ones_like(xx)
        ax.plot_wireframe(xx, yy, zz, color=color)
        ax.plot_surface(xx, yy, zz, color=color, alpha=0.2)
        yy = y_range[1] * np.ones_like(xx)
        ax.plot_wireframe(xx, yy, zz, color=color)
        ax.plot_surface(xx, yy, zz, color=color, alpha=0.2)


    def volume(self):
        return ((self.x_max - self.x_min) * (self.y_max - self.y_min)
                * (self.z_max - self.z_min))



def subtract_from_all(current_state, new_prism):
    result = set()
    for prism in current_state:
        differences = prism - new_prism
        result = result.union(differences)
    return result


def add_to_all(current_state, new_prism):
    result = subtract_from_all(current_state, new_prism)
    result.add(new_prism)
    return result

if __name__ == '__main__':
    main()
