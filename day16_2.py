# faster version of part 2, but does not work for all inputs

import sys

with open("input16") as f:
    n = [int(x) for x in f.read()]

k = int("".join([str(x) for x in n[:7]]))

if k <= 10000 * len(n) / 2:
    print("this won't work")
    sys.exit(0)

total_len = 10000 * len(n)
relevant_len = total_len - k
offset = k % len(n)

l = n[offset:] + (relevant_len // len(n)) * n

for i in range(100):
    print(i)
    c_sum = 0
    l_new = []
    for m in reversed(l):
        c_sum += m
        c_sum %= 10
        l_new.append(c_sum)
    l = list(reversed(l_new))

print("".join([str(x) for x in l[:8]]))