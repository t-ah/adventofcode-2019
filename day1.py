def fuel(start):
    current = start // 3 - 2
    while current > 0:
        yield current
        current = current // 3 - 2

with open("input1") as f:
    lines = f.readlines()

result = 0
for mass in lines:
    result += sum(fuel(int(mass)))

print(result)