from collections import defaultdict, deque
import sys

def neighbours(node, grid, shortcuts):
    results = []
    (x,y) = node
    for n in [(x, y+1), (x,y-1), (x+1,y), (x-1,y)]:
        if n in grid:
            results.append(n)
    return results + shortcuts[node]

with open("input20") as f:
    input_grid = [list(x.replace("\n", "")) for x in f.readlines()]

grid = defaultdict(int)
portals = defaultdict(lambda: list())
max_y = len(input_grid)
max_x = len(input_grid[0])
for y in range(max_y):
    for x in range(max_x):
        c = input_grid[y][x]
        if c == ".":
            grid[(x,y)] = 1
        elif c.isalpha():
            if y < max_y - 1:
                d = input_grid[y + 1][x]
                if d.isalpha():
                    if y > 0 and input_grid[y - 1][x] == ".":
                        portals[c+d].append((x, y - 1))
                    else:
                        portals[c+d].append((x, y + 2))
                    continue
            if x < max_x -1:
                d = input_grid[y][x + 1]
                if d.isalpha():
                    if x > 0 and input_grid[y][x - 1] == ".":
                        portals[c+d].append((x - 1, y))
                    else:
                        portals[c+d].append((x + 2, y))
                    continue

start = portals["AA"][0]
end = portals["ZZ"][0]

shortcuts = defaultdict(lambda: list())
for connection in portals.values():
    if len(connection) == 2:
        shortcuts[connection[0]].append(connection[1])
        shortcuts[connection[1]].append(connection[0])

distances = defaultdict(lambda: sys.maxsize)
distances[start] = 0

expand = deque()
expand.append(start)
while len(expand) > 0:
    node = expand.pop()
    node_dist = distances[node]
    for n in neighbours(node, grid, shortcuts):
        if node_dist + 1 < distances[n]:
            distances[n] = node_dist + 1
            expand.append(n)
print(distances[end])