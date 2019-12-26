def reverse(deck):
    return list(reversed(deck))

def deal_with_increment(deck, increment):
    d = len(deck)
    new_deck = d * [0]
    for i in range(d):
        new_deck[(i * increment) % d] = deck[i]
    return new_deck

def cut(deck, c):
    return deck[c:] + deck[:c]

with open("input22") as f:
    lines = f.readlines()

cards = 10007
deck = [i for i in range(cards)]

for line in lines:
    op = line.strip().split(" ")
    if op[1] == "into": # reverse
        deck = reverse(deck)
    elif op[1] == "with":
        increment = int(op[3])
        deck = deal_with_increment(deck, increment)
    elif op[0] == "cut":
        c = int(op[1])
        deck = cut(deck, c)

for pos, card in enumerate(deck):
    if card == 2019:
        print(pos)
        break

def shuffle(instructions, position, cards):
    index = position
    for op in instructions:
        if op[1] == "into":
            index = cards - (index + 1)
        elif op[1] == "with":
            increment = int(op[3]) % cards
            index = (index * increment) % cards
        else:
            index = (index + (cards - int(op[1]))) % cards
    return index

instructions = [line.strip().split(" ") for line in lines]
cards = 119315717514047
times = 101741582076661

print(shuffle(instructions, 2019, 10007)) # part 1 optimised