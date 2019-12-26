def parse():
    with open("input16") as f:
        n = [int(x) for x in f.read()]
    return n

n = parse()

for _ in range(100):
    result = []
    for i in range(1, len(n) + 1):
        digit = 0
        start = i - 1
        add = 1
        while start < len(n):
            end = min(start + i, len(n))
            digit += add * sum(n[start:end])
            add *= -1
            start += 2*i
        result.append(abs(digit) % 10)
    n = result

print("".join([str(x) for x in n[:8]]))

# part 2

n = parse()
k = int("".join([str(x) for x in n[:7]]))
total_len = 10000 * len(n)
relevant_len = total_len - k
offset = k % len(n)
l = n[offset:] + (relevant_len // len(n)) * n

for nr in range(100):
    print(nr)
    result = []
    cache = {}
    for i in range(0, len(l)):
        digit = 0
        start = i
        add = 1
        while start < len(l):
            end = min(start + i + k, len(l))
            if (start - 1, end) in cache:
                q = (cache[(start - 1,end)] - l[start - 1])
            else:
                q = sum(l[start:end])
            digit += add * q
            cache[(start, end)] = q
            add *= -1
            start += 2 * (i + k)
        result.append(abs(digit) % 10)
    l = result

print("".join([str(x) for x in l[:8]]))