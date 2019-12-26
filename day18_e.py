from collections import defaultdict, deque
import string

def surrounding(pos):
    return [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]


def next_elements(element, distances, doors, min_distances, best):
    new_elements = []
    path = element["keys"]
    missing = set(string.ascii_lowercase) - set(path)
    # min_remaining = sum([min_distances[x] for x in missing])
    # if element["steps"] + min_remaining >= best:
    #     return []
    for m in missing:
        blocked = False
        for door in doors[(path[-1], m)]:
            if door.lower() not in path:
                blocked = True
                break
        if not blocked:
            new_elements.append({"keys": path + m, "steps": element["steps"] + distances[(path[-1] ,m)]})
    return new_elements

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
                keys['@'] = (x,y)
            else:
                grid[(x,y)] = c

# assume there is only 1 path between each 2 nodes
distances = defaultdict(int)
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

min_distances = {}
for c in keys:
    min_d = 10000
    for d in keys:
        if d == c: continue
        if distances[(c,d)] < min_d:
            min_d = distances[(c,d)]
    min_distances[c] = min_d


# start_element = {"keys": "@", "steps": 0}

# incomplete_elements = deque()
# incomplete_elements.append(start_element)

# result = {"keys": "", "steps": 10000}


def find_shortest(path, missing, doors, cache):
    position = path[-1]
    if len(missing) == 1:
        return distances[(position, missing.pop())]
    cache_key = position + "".join(sorted(list(missing)))
    if cache_key in cache:
        return cache[cache_key]
    results = []
    for m in missing:
        blocked = False
        for door in doors[(position[-1], m)]:
            if door.lower() not in path:
                blocked = True
                break
        if not blocked:
            dist = find_shortest(path + m, missing - set(m), doors, cache)
            if dist:
                results.append(distances[(position, m)] + dist)
    if len(results) == 0:
        return
    result = min(results)
    cache[cache_key] = result
    return result

cache = {}
res = find_shortest('@', set(string.ascii_lowercase), doors, cache)
print(res)

# while len(incomplete_elements) > 0:
#     elem = incomplete_elements.pop()
#     if elem["steps"] >= result["steps"]: continue
#     new_elems = next_elements(elem, distances, doors, min_distances, result["steps"])
#     for e in new_elems:
#         if len(e["keys"]) == len(keys):
#             if e["steps"] < result["steps"]:
#                 result = e
#             print(e, result["steps"])
#         else:
#             if e["steps"] < result["steps"]:
#                 incomplete_elements.append(e)
# print(result)