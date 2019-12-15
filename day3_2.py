from collections import defaultdict
import sys

with open("input3") as f:
    wires = f.readlines()

moves = {"U": (0,-1), "D": (0,1), "L": (-1,0), "R": (1,0)}

grids = [defaultdict(int),defaultdict(int)]
for i in range(2):
    step = 0
    current = (0,0)
    directions = wires[i].split(",")
    for d in directions:
        length = int(d[1:])
        direction = d[:1]
        for _ in range(length):
            step += 1
            m = moves[direction]
            current = (current[0] + m[0], current[1] + m[1])
            if grids[i][current] == 0:
                grids[i][current] = step

result = sys.maxsize
for k in grids[0]:
    if k in grids[1]:
        steps = grids[0][k] + grids[1][k]
        if steps < result:
            result = steps
print(result)