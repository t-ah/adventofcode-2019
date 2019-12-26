def count_bugs(grid, pos):
    c = 0
    if pos % 5 > 0 and grid[pos - 1] == '#':
        c += 1
    if pos % 5 < 4 and grid[pos + 1] == '#':
        c += 1
    if pos > 4 and grid[pos - 5] == '#':
        c += 1
    if pos < 20 and grid[pos + 5] == '#':
        c += 1
    return c


with open("input24") as f:
    grid = [c for c in f.read().replace("\n", "")]

layouts = set()
while True:
    new_grid = grid.copy()
    for i in range(25):
        c = count_bugs(grid, i)
        if new_grid[i] == '#':
            if c != 1:
                new_grid[i] = '.'
        else:
            if c == 1 or c == 2:
                new_grid[i] = '#'
    grid = new_grid
    result = 0
    for i in range(25):
        if grid[i] == '#':
            result += 2**i
    if result in layouts:
        print(result)
        break
    layouts.add(result)