from math import atan2, degrees, hypot
from collections import defaultdict
import sys

def isBetween(a, b, c):
    crossprod = (c[1] - a[1]) * (b[0] - a[0]) - (c[0] - a[0]) * (b[1] - a[1])
    if crossprod != 0:
        return False
    dotprod = (c[0] - a[0]) * (b[0] - a[0]) + (c[1] - a[1]) * (b[1] - a[1])
    if dotprod < 0:
        return False
    if dotprod > (b[0] - a[0]) * (b[0] - a[0]) + (b[1] - a[1]) * (b[1] - a[1]):
        return False
    return True

def getClosest(a1, moreA):
    if len(moreA) == 0: return None
    minDist = sys.maxsize
    best = None
    for a2 in moreA:
        dist = hypot(a2[0] - a1[0], a2[1] - a1[1])
        if dist < minDist:
            minDist = dist
            best = a2
    return best

# parse
with open("input10") as f:
    rows = f.readlines()
asteroids = []
for y in range(len(rows)):
    row = rows[y]
    for x in range(len(row)):
        if row[x] == "#":
            asteroids.append((x,y))

# process
results = {}
maxCount = 0
bestAst = (13,17)

if bestAst == (-1,-1): # part 1
    for a1 in asteroids:
        print(a1)
        count = 0
        for a2 in asteroids:
            if a2 == a1: continue
            blocked = False
            for a3 in asteroids:
                if a3 == a1 or a3 == a2: continue
                if isBetween(a1, a2, a3):
                    blocked = True
                    break
            if not blocked:
                count += 1
        results[a1] = count
        if count > maxCount:
            maxCount = count
            bestAst = a1
    print(bestAst, maxCount)

# part 2
asteroids.remove(bestAst)
angleSet = set()
byAngle = defaultdict(lambda: list())
for a1 in asteroids:
    angle = (270 + degrees(atan2((bestAst[1] - a1[1]), (bestAst[0] - a1[0])))) % 360
    angleSet.add(angle)
    byAngle[angle].append(a1)

angles = list(angleSet)
angles.sort()
count = 0
found = False
while not found:
    for angle in angles:
        asts = byAngle[angle]
        c = getClosest(bestAst, asts)
        if c != None:
            asts.remove(c)
            count += 1
            if count == 200:
                print(c)
                found = True
                break