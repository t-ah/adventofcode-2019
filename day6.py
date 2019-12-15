from collections import defaultdict

def count_orbits(is_orbiting, o_counts, name):
    if name in o_counts:
        return o_counts[name]
    else:
        return 1 + count_orbits(is_orbiting, o_counts, is_orbiting[name])

def path_to_com(name, is_orbiting):
    path = set()
    node = name
    while(True):
        path.add(node)
        if node == "COM":
            return path
        node = is_orbiting[node]

with open("input6") as f:
    lines = f.readlines()

is_orbiting = {}
o_counts = defaultdict(int)
o_counts["COM"] = 0

for line in lines:
    orbits = line.strip().split(")")
    is_orbiting[orbits[1]] = orbits[0]

result = 0
for orbiter in is_orbiting:
    o_counts[orbiter] = count_orbits(is_orbiting, o_counts, orbiter)
    result += o_counts[orbiter]
print(result)

start = is_orbiting["YOU"]
end = is_orbiting["SAN"]

path1 = path_to_com(start, is_orbiting)
path2 = path_to_com(end, is_orbiting)

inters = path1.intersection(path2)
nodes1 = path1.difference(inters)
nodes2 = path2.difference(inters)

result = len(nodes1) + len(nodes2)
print(result)