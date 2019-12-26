from collections import defaultdict, deque
import sys

def neighbours(position, grid, shortcuts, inner, outer):
    (node, layer) = position
    results = []
    (x,y) = node
    for n in [(x, y+1), (x,y-1), (x+1,y), (x-1,y)]:
        if n in grid:
            results.append((n, layer))
    if node in outer and layer > 0:
        results.append((shortcuts[node][0], layer-1))
    elif node in inner:
        results.append((shortcuts[node][0], layer+1))
    return results

with open("input20") as f:
    input_grid = [list(x.replace("\n", "")) for x in f.readlines()]

grid = defaultdict(int)
portals = defaultdict(lambda: list())
outer_ports = set()
inner_ports = set()
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
                        if y == max_y - 2: outer_ports.add((x, y-1))
                        else: inner_ports.add((x, y-1))
                    else:
                        portals[c+d].append((x, y + 2))
                        if y == 0: outer_ports.add((x, y+2))
                        else: inner_ports.add((x, y+2))
                    continue
            if x < max_x -1:
                d = input_grid[y][x + 1]
                if d.isalpha():
                    if x > 0 and input_grid[y][x - 1] == ".":
                        portals[c+d].append((x - 1, y))
                        if x == max_x - 2: outer_ports.add((x-1, y))
                        else: inner_ports.add((x-1, y))
                    else:
                        portals[c+d].append((x + 2, y))
                        if x == 0: outer_ports.add((x+2, y))
                        else: inner_ports.add((x+2, y))
                    continue

start = portals["AA"][0]
end = portals["ZZ"][0]
outer_ports.remove(start)
outer_ports.remove(end)

shortcuts = defaultdict(lambda: list())
for connection in portals.values():
    if len(connection) == 2:
        shortcuts[connection[0]].append(connection[1])
        shortcuts[connection[1]].append(connection[0])

visited = set()
visited.add((start,0))
expand = set()
expand.add((start,0))

steps = 0
while True:
    steps += 1
    new_nodes = set()
    for node in expand:
        for next_node in neighbours(node, grid, shortcuts, inner_ports, outer_ports):
            if next_node not in visited:
                visited.add(next_node)
                new_nodes.add(next_node)
    expand = new_nodes
    if (end, 0) in expand:
        print(steps)
        break