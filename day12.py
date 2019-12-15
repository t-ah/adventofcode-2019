moons = []
with open("input12") as f:
    for line in f.readlines():
        moons.append([int(x) for x in line.strip()[1:-1].replace("x", "").replace("y","").replace("z","").replace("=","").split(", ")] + [0,0,0])

for _ in range(1000):
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

result = sum([sum([abs(x) for x in moon[:3]]) * sum([abs(x) for x in moon[3:]]) for moon in moons])
print(result)
# 3088 too low