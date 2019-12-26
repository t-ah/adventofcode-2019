from collections import defaultdict

def get_right(x,y,l):
    if x == 1 and y == 2:
        return [(0,y,l+1) for y in range(5)]
    if x == 4:
        return [(3,2,l-1)]
    return [(x+1,y,l)]

def get_left(x,y,l):
    if x == 3 and y == 2:
        return [(4,y,l+1) for y in range(5)]
    if x == 0:
        return [(1,2,l-1)]
    return [(x-1,y,l)]

def get_above(x,y,l):
    if x == 2 and y == 3:
        return [(x,4,l+1) for x in range(5)]
    if y == 0:
        return [(2,1,l-1)]
    return [(x,y-1,l)]

def get_below(x,y,l):
    if x == 2 and y == 1:
        return [(x,0,l+1) for x in range(5)]
    if y == 4:
        return [(2,3,l-1)]
    return [(x,y+1,l)]

def adjacent(pos):
    return get_left(*pos) + get_right(*pos) + get_above(*pos) + get_below(*pos)

def get_bugs(state, iterations):
    bugs = set()
    for i in range(len(state)):
        if state[i] == '#':
            bugs.add((i % 5, i // 5, 0))

    for _ in range(iterations):
        new_bugs = set()
        influences = defaultdict(int)
        for bug in bugs:
            for a in adjacent(bug):
                influences[a] += 1
        for bug in bugs:
            if influences[bug] == 1:
                new_bugs.add(bug)
        for pos, inf in influences.items():
            if pos not in bugs and (inf == 1 or inf == 2):
                new_bugs.add(pos)
        bugs = new_bugs
    return len(bugs)

print(get_bugs("....##..#.#.?##..#..#....", 10) == 99)

with open("input24") as f:
    state = f.read().replace("\n", "")

print(get_bugs(state, 200))