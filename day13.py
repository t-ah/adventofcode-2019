from collections import defaultdict

def parse(filename):
    mem = defaultdict(int)
    with open(filename) as f:
        prog = [int(x) for x in f.read().strip().split(",")]
        for i in range(len(prog)):
            mem[i] = prog[i]
    return mem

def createEmptyState(name, mem):
    return {"nr": name, "pc": 0, "inputs": [], "mem": mem, "done": False, "base": 0}

def get_addr(mem, pc, instr, index, rel_base):
    if len(instr) > index + 1:
        if instr[-2 - index] == "1":
            return pc + index
        elif instr[-2 - index] == "2":
            return mem[pc + index] + rel_base
    return mem[pc + index]

def draw_grid(grid):
    x_min = min(grid.keys(), key = lambda t: t[0])[0]
    x_max = max(grid.keys(), key = lambda t: t[0])[0]
    y_min = min(grid.keys(), key = lambda t: t[1])[1]
    y_max = max(grid.keys(), key = lambda t: t[1])[1]

    for y in range(y_min, y_max + 1):
        row = ""
        for x in range(x_min, x_max):
            row += str(grid[(x,y)])
        print(row.replace("0", " "))

def runProg(state):
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

# part 1

mem = parse("input13")
state = createEmptyState(1, mem.copy())
grid = defaultdict(int)

while not state["done"]:
    result = runProg(state)
    #print(result)
    for i in range(0, len(result), 3):
        grid[(result[i], result[i+1])] = result[i+2]

print(list(grid.values()).count(2))
draw_grid(grid)

# part 2

mem[0] = 2
state = createEmptyState(2, mem)
grid = defaultdict(int)
score = 0
ball = (0,0)
paddle = (0,0)

while not state["done"]:
    result = runProg(state)
    for i in range(0, len(result), 3):
        pos = (result[i], result[i+1])
        if pos == (-1,0):
            score = result[i+2]
            if list(grid.values()).count(2) == 0:
                print("final score", score)
        else:
            grid[pos] = result[i+2]
            if result[i+2] == 4:
                ball = pos
            elif result[i+2] == 3:
                paddle = pos
            #draw_grid(grid)

    # sophisticated paddle AI
    if paddle[0] < ball[0]:
        state["inputs"] += [1]
    elif paddle[0] > ball[0]:
        state["inputs"] += [-1]
    else:
        state["inputs"] += [0]
