def check_conditions(digits):
    same_cond = False
    for i in range(len(digits) - 1):
        if digits[i + 1] < digits[i]:
            return False
        if digits[i + 1] == digits[i]:
            if i == 0 or digits[i - 1] != digits[i]:
                if i == len(digits) - 2 or digits[i + 2] != digits[i]:
                    same_cond = True
    return same_cond

result = 0
for i in range(146810, 612564 + 1):
    digits = [int(x) for x in str(i)]
    if check_conditions(digits):
        result += 1
print(result)