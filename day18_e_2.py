from collections import defaultdict, deque
import string

def surrounding(pos):
    return [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]

grid = defaultdict(int)
start = (-1,-1)
keys = {}
with open("input18") as f:
    lines = f.readlines()
    for y in range(len(lines)):
        line = lines[y]
        for x in range(len(line)):
            c = line[x]
            if c == "#": continue
            if c.islower():
                keys[c] = (x,y)
            if c == '@':
                grid[(x,y)] = '.'
                start = (x,y)
            else:
                grid[(x,y)] = c

(sx, sy) = start
for x in [(sx,sy), (sx-1,sy), (sx+1,sy), (sx,sy+1), (sx,sy-1)]:
    del(grid[x])

keys["0"] = (sx - 1, sy - 1)
keys["1"] = (sx + 1, sy - 1)
keys["2"] = (sx - 1, sy + 1)
keys["3"] = (sx + 1, sy + 1)

# assume there is only 1 path between each 2 nodes
distances = {}
doors = defaultdict(lambda: list())
for c in keys:
    c_pos = keys[c]
    to_expand = deque()
    to_expand.append((c_pos,[]))
    visited = set()
    visited.add(c_pos)
    steps = 0
    while len(to_expand) > 0:
        steps += 1
        new_nodes = deque()
        for expand in to_expand:
            for pos in surrounding(expand[0]):
                if pos in grid and pos not in visited:
                    visited.add(pos)
                    new_node = (pos, expand[1].copy())
                    c_n = grid[pos]
                    if c_n.isalpha():
                        if c_n.islower(): # key
                            distances[(c,c_n)] = steps
                            doors[(c,c_n)] = set(expand[1])
                        else:
                            new_node[1].append(c_n)
                    new_nodes.append(new_node)
        to_expand = new_nodes

def reachable_by(goal, distances):
    for i in ['0','1','2','3']:
        if (i,goal) in distances:
            return i
    return -1

def find_shortest(paths, missing, doors, cache):
    positions = [path[-1] for path in paths]
    if len(missing) == 1:
        last_node = missing.pop()
        robot = reachable_by(last_node, distances)
        return distances[(positions[int(robot)], last_node)]
    cache_key = "".join(positions) + "".join(sorted(list(missing)))
    if cache_key in cache:
        #print("cache hit", cache_key)
        return cache[cache_key]
    results = []
    for m in missing:
        robot = reachable_by(m, distances)
        blocked = False
        for door in doors[(positions[int(robot)], m)]:
            if door.lower() not in "".join(paths):
                blocked = True
                break
        if not blocked:
            new_paths = paths.copy()
            new_paths[int(robot)] += m
            dist = find_shortest(new_paths, missing - set(m), doors, cache)
            if dist:
                results.append(distances[(positions[int(robot)], m)] + dist)
    if len(results) == 0:
        return
    result = min(results)
    cache[cache_key] = result
    return result

paths = ['0','1','2','3']
cache = {}
res = find_shortest(paths, set(string.ascii_lowercase), doors, cache)
print(res)