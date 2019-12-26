from collections import defaultdict

def parse(filename):
    mem = defaultdict(int)
    with open(filename) as f:
        prog = [int(x) for x in f.read().strip().split(",")]
        for i in range(len(prog)):
            mem[i] = prog[i]
    return mem

def create_state(name, mem):
    return {"name": name, "pc": 0, "inputs": [], "mem": mem, "done": False, "base": 0}

def get_addr(mem, pc, instr, index, rel_base):
    if len(instr) > index + 1:
        if instr[-2 - index] == "1":
            return pc + index
        elif instr[-2 - index] == "2":
            return mem[pc + index] + rel_base
    return mem[pc + index]

def run_prog(state, direct_print):
    if state["done"]: return []
    pc = state["pc"]
    base = state["base"]
    mem = state["mem"]
    outputs = []

    while True:
        instr = str(mem[pc])
        op = instr[-1]
        if op == "1":
            mem[get_addr(mem, pc, instr, 3, base)] = mem[get_addr(mem, pc, instr, 1, base)] + mem[get_addr(mem, pc, instr, 2, base)]
            pc += 4
        elif op == "2":
            mem[get_addr(mem, pc, instr, 3, base)] = mem[get_addr(mem, pc, instr, 1, base)] * mem[get_addr(mem, pc, instr, 2, base)]
            pc += 4
        elif op == "3":
            if len(state["inputs"]) > 0:
                mem[get_addr(mem, pc, instr, 1, base)] = state["inputs"].pop(0)
                pc += 2
            else: # wait for new inputs
                break
        elif op == "4":
            output = mem[get_addr(mem, pc, instr, 1, base)]
            if direct_print and output == 10:
                print("".join([chr(x) for x in outputs]))
                outputs = []
            else:
                outputs.append(output)
            pc += 2
        elif op == "5":
            if mem[get_addr(mem, pc, instr, 1, base)] != 0:
                pc = mem[get_addr(mem, pc, instr, 2, base)]
            else:
                pc += 3
        elif op == "6":
            if mem[get_addr(mem, pc, instr, 1, base)] == 0:
                pc = mem[get_addr(mem, pc, instr, 2, base)]
            else:
                pc += 3
        elif op == "7":
            v = 0
            if mem[get_addr(mem, pc, instr, 1, base)] < mem[get_addr(mem, pc, instr, 2, base)]:
                v = 1
            mem[get_addr(mem, pc, instr, 3, base)] = v
            pc += 4
        elif op == "8":
            v = 0
            if mem[get_addr(mem, pc, instr, 1, base)] == mem[get_addr(mem, pc, instr, 2, base)]:
                v = 1
            mem[get_addr(mem, pc, instr, 3, base)] = v
            pc += 4
        elif op == "9":
            if len(instr) >= 2 and instr[-2] == "9":
                state["done"] = True
                break
            else:
                base += mem[get_addr(mem, pc, instr, 1, base)]
                pc += 2
        else:
            print(f"Unknown command {mem[pc]:d}")
            break
    state["pc"] = pc
    state["base"] = base
    return outputs

def move(pos, direction):
    return (pos[0] + direction[0], pos[1] + direction[1])

def find_compression(res):
    for len_A in range(1,11):
        word_A = res[:len_A]
        after_A = res.replace(word_A, "A")
        first_not_A = -1
        for i in range(0, len(after_A)):
            if after_A[i] != 'A':
                first_not_A = i
                break
        for len_B in range(1, 11):
            word_B = after_A[first_not_A:first_not_A + len_B]
            if 'A' in word_B:
                # print("no solution for B")
                break
            after_B = after_A.replace(word_B, "B")
            first_not_AB = -1
            for i in range(0, len(after_B)):
                if after_B[i] not in "AB":
                    first_not_AB = i
                    break
            for len_C in range(1, 11):
                word_C = after_B[first_not_AB:first_not_AB + len_C]
                after_C = after_B.replace(word_C, "C")
                correct = all(c in "ABC" for c in after_C)
                if correct:
                    return(after_C, word_A, word_B, word_C)

mem = parse("input17")
state = create_state("", mem.copy())
outputs = run_prog(state, False)

line = ""
x = 0
y = 0
grid = defaultdict(int)
for c in outputs:
    if c == ord('#'):
        line += "#"
        grid[(x,y)] = 1
        x += 1
    elif c == ord('.'):
        line += "."
        #grid[(x,y)] = 0
        x += 1
    elif c == 10:
        print(line)
        line = ""
        x = 0
        y += 1
    else:
        robot_direction = c
        robot_position = (x,y)
        line += "?"
        grid[(x,y)] = 1
        x += 1
print("")

result = 0
for (x,y) in grid:
    if (x + 1, y) in grid and (x - 1, y) in grid and (x, y + 1) in grid and (x, y - 1) in grid:
        result += x * y
print(result)

# part 2

directions = [(0,-1), (1,0), (0,1), (-1,0)]
ascii_to_direction = {94: 0, 62: 1, 118: 2, 60: 3}

# find path
path = []
direction = ascii_to_direction[robot_direction]
steps = 0
while True:
    new_position = move(robot_position, directions[direction])
    if new_position in grid:
        steps += 1
        robot_position = new_position
    else:
        if steps > 0:
            for c in str(steps):
                path.append(ord(c))
        steps = 1
        direction = (direction + 1) % 4
        new_position = move(robot_position, directions[direction])
        if new_position in grid:
            path.append(ord('R'))
        else:
            direction = (direction + 2) % 4
            new_position = move(robot_position, directions[direction])
            if new_position in grid:
                path.append(ord('L'))
            else:
                break
        robot_position = new_position

# compress path
res = "".join([chr(x) for x in path])
comp = find_compression(res)
inputs = []
for elem in comp:
    for i in range(len(elem)):
        c_i = elem[i]
        if i > 0 and not(c_i.isdigit() and elem[i-1].isdigit()):
            inputs.append(44)
        inputs.append(ord(c_i))
    inputs.append(10)
inputs += [ord('n'), 10]

mem[0] = 2
state = create_state("", mem)
state["inputs"] = inputs
final_result = run_prog(state, True)
print(final_result[0])