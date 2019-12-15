from math import gcd
from functools import reduce

def lcm(numbers):
    return reduce(lambda a, b: a * b // gcd(a,b), numbers)

moons = []
with open("input12") as f:
    for line in f.readlines():
        moons.append([int(x) for x in line.strip()[1:-1].replace("x", "").replace("y","").replace("z","").replace("=","").split(", ")] + [0,0,0])

start = [[moon[m] for moon in moons] + ([0] * len(moons)) for m in range(3)]
step = 1
result = [0] * 3
while True:
    for moon in moons:
        for i in range(3):
            count = 0
            for other_moon in moons:
                if other_moon[i] > moon[i]:
                    count += 1
                elif other_moon[i] < moon[i]:
                    count -= 1
            moon[i + 3] += count
    for moon in moons:
        for i in range(3):
            moon[i] += moon[i + 3]
    for m in range(3):
        state = [moon[m] for moon in moons] + [moon[m + 3] for moon in moons]
        if state == start[m]:
            if result[m] == 0:
                result[m] = step
                print(step)
    if result[0] != 0 and result[1] != 0 and result[2] != 0:
        break
    step += 1

print(lcm(result))