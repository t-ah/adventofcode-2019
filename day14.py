from collections import defaultdict, deque
import math

def parse(file_name):
    reqs = {}
    with open(file_name) as f:
        for line in f.readlines():
            lr = line.strip().split(" => ")
            result = lr[1].split(" ")
            req = [(item[1], int(item[0])) for item in map(lambda x: x.split(" "), lr[0].split(", "))]
            reqs[result[1]] = (int(result[0]), req)
    return reqs

recipes = parse("input14")
storage = defaultdict(int)
reqs = deque(recipes["FUEL"][1])
ores = 0

while len(reqs) != 0:
    req = reqs.pop()
    req_name = req[0]
    recipe = recipes[req_name]
    quantity_necessary = req[1]
    available = min(quantity_necessary, storage[req_name])
    storage[req_name] -= available
    quantity_necessary -= available
    applications = math.ceil(quantity_necessary / recipe[0])
    for new_req in recipe[1]:
        if new_req[0] == "ORE":
            ores += applications * new_req[1]
        else:
            reqs.append((new_req[0], applications * new_req[1]))
    surplus = applications * recipe[0] - quantity_necessary
    storage[req_name] += surplus

print(ores, "ORE necessary")

# part 2

def works(n, recipes):
    storage = defaultdict(int)
    start = recipes["FUEL"][1]
    reqs = deque([(x[0], n * x[1]) for x in start])
    storage["ORE"] = 1000000000000
    while len(reqs) != 0:
        req = reqs.pop()
        req_name = req[0]
        quantity_necessary = req[1]
        available = min(quantity_necessary, storage[req_name])
        storage[req_name] -= available
        quantity_necessary -= available
        if quantity_necessary == 0:
            continue
        if req_name == "ORE":
            return False
        recipe = recipes[req_name]
        applications = math.ceil(quantity_necessary / recipe[0])
        for new_req in recipe[1]:
            reqs.append((new_req[0], applications * new_req[1]))
        surplus = applications * recipe[0] - quantity_necessary
        storage[req_name] += surplus
    return True

# simple binary search
n_min = 1000000000000 // ores
n_max = 1000000000000
while True:
    n = n_min + (n_max - n_min) // 2
    if n == n_min:
        print(n_min, "FUEL created")
        break
    if (works(n, recipes)):
        n_min = n
    else:
        n_max = n