from collections import defaultdict

with open("input3") as f:
    wires = f.readlines()

moves = {"U": (0,-1), "D": (0,1), "L": (-1,0), "R": (1,0)}

grid = defaultdict(int)
for i in range(2):
    current = (0,0)
    directions = wires[i].split(",")
    for d in directions:
        length = int(d[1:])
        direction = d[:1]
        for _ in range(length):
            m = moves[direction]
            current = (current[0] + m[0], current[1] + m[1])
            if i == 0:
                grid[current] = 1
            elif grid[current] == 1:
                grid[current] = 2

result = (0,0)
for k in grid:
    if grid[k] == 2:
        if result == (0,0):
            result = k
        elif abs(k[0]) + abs(k[1]) < abs(result[0]) + abs(result[1]):
            result = k
print(sum([abs(x) for x in result]))