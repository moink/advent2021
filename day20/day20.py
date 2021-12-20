import advent_tools


def main():
    data = advent_tools.read_input_line_groups()
    grid, algo = process_input(data)
    print('Part 1:', run_part(grid, algo, 2))
    print('Part 2:', run_part(grid, algo, 50))


def process_input(data):
    algo = [0 if char == "." else 1 for char in data[0][0]]
    grid = advent_tools.PlottingGrid.from_str(text=data[1])
    return grid, algo


def run_part(grid, algo, steps):
    off_edges_val = 0
    for _ in range(steps):
        n, m = grid.grid.shape
        new_grid = advent_tools.PlottingGrid((n + 2, m + 2))
        for j in range(-1, n + 1):
            for i in range(-1, m + 1):
                nums = []
                for jj in range(j - 1, j + 2):
                    for ii in range(i - 1, i + 2):
                        if 0 <= jj < n and 0 <= ii < m:
                            val = grid.grid[jj, ii]
                        else:
                            val = off_edges_val
                        nums.append(str(val))
                lookup_val = int("".join(nums), 2)
                new_grid.grid[j + 1, i + 1] = algo[lookup_val]
        grid = new_grid
        if off_edges_val == 0:
            off_edges_val = algo[0]
        else:
            off_edges_val = algo[-1]
        grid.draw()
    grid.show()
    return grid.sum().sum()


if __name__ == '__main__':
    main()