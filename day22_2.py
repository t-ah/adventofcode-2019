# with not insignificant help
# TODO: how does modinv work exactly?

with open("input22") as f:
    lines = f.readlines()

instructions = [line.strip().split(" ") for line in lines]
pos = 2020
cards = 119315717514047
times = 101741582076661

# shuffle in reverse
def shuffle(instructions, position, cards):
    index = position
    for op in reversed(instructions):
        if op[1] == "into":
            index = cards - (index + 1)
        elif op[1] == "with":
            increment = int(op[3]) % cards
            index = (modinv(increment, cards) * index) % cards
        else:
            cut = -int(op[1])
            index = (index + (cards - cut)) % cards
    return index

def modinv(a, m):
    return pow(a, m-2, m)

fx = shuffle(instructions, pos, cards)
f2x = shuffle(instructions, fx, cards)

a = ((fx - f2x) * modinv(pos-fx+cards, cards)) % cards
b = fx - (a * pos)

print((pow(a, times, cards) * pos + (pow(a, times, cards)-1) * modinv(a - 1, cards) * b) % cards)