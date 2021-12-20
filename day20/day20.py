import advent_tools


def main():
    data = advent_tools.read_input_line_groups()
    grid, algo = process_input(data)
    print('Part 1:', run_part(grid, algo, 2))
    print('Part 2:', run_part(grid, algo, 50))


def process_input(data):
    algo = [0 if char == "." else 1 for char in data[0][0]]
    grid = advent_tools.PlottingGrid.from_lines(lines=data[1])
    return grid, algo


def run_part(grid, algo, steps):
    off_edges_val = 0
    for _ in range(steps):
        grid, off_edges_val = take_one_step(grid, algo, off_edges_val)
        grid.draw()
    grid.show()
    return grid.sum().sum()


def take_one_step(grid, algo, off_edges_val):
    n, m = grid.grid.shape
    new_grid = advent_tools.PlottingGrid((n + 2, m + 2))
    for j in range(-1, n + 1):
        for i in range(-1, m + 1):
            lookup_val = solve_for_position(grid, i, j, off_edges_val)
            new_grid.grid[j + 1, i + 1] = algo[lookup_val]
    grid = new_grid
    if off_edges_val == 0:
        off_edges_val = algo[0]
    else:
        off_edges_val = algo[-1]
    return grid, off_edges_val


def solve_for_position(grid, i, j, off_edges_val):
    n, m = grid.grid.shape
    nums = []
    for jj in range(j - 1, j + 2):
        for ii in range(i - 1, i + 2):
            if 0 <= jj < n and 0 <= ii < m:
                val = grid.grid[jj, ii]
            else:
                val = off_edges_val
            nums.append(str(val))
    return int("".join(nums), 2)


if __name__ == '__main__':
    main()
