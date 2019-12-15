def check_conditions(digits):
    same_cond = False
    for i in range(len(digits) - 1):
        first = int(digits[i])
        second = int(digits[i + 1])
        if second < first:
            return False
        elif second == first:
            same_cond = True
    return same_cond

result = 0
for i in range(146810, 612564 + 1):
    digits = str(i)
    if check_conditions(digits):
        result += 1
print(result)