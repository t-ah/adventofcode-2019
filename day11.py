from collections import defaultdict

def parse(filename):
    mem = defaultdict(int)
    with open(filename) as f:
        prog = [int(x) for x in f.read().strip().split(",")]
        for i in range(len(prog)):
            mem[i] = prog[i]
    return mem

def createEmptyState(name):
    return {"nr": name, "pc": 0, "inputs": [], "mem": mem, "done": False, "base": 0}

def get_addr(mem, pc, instr, index, rel_base):
    if len(instr) > index + 1:
        if instr[-2 - index] == "1":
            return pc + index
        elif instr[-2 - index] == "2":
            return mem[pc + index] + rel_base
    return mem[pc + index]

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

mem = parse("input11")
state = createEmptyState(1)

grid = defaultdict(int)
position = (0,0)
turn_index = 0
turns = [(0,-1), (1,0), (0,1), (-1,0)]
painted_cells = set()
while not state["done"]:
    result = runProg(state)
    for i in range(0, len(result), 2):
        grid[position] = result[i]
        painted_cells.add(position)
        if result[i+1] == 0:
            turn_index = (turn_index - 1) % 4
        else:
            turn_index = (turn_index + 1) % 4
        step = turns[turn_index]
        position = (position[0] + step[0], position[1] + step[1])
    state["inputs"].append(grid[position])
print(len(painted_cells))

position = (0,0)
turn_index = 0
grid = defaultdict(int)
grid[(0,0)] = 1
state = createEmptyState(2)

while not state["done"]:
    result = runProg(state)
    for i in range(0, len(result), 2):
        grid[position] = result[i]
        if result[i+1] == 0:
            turn_index = (turn_index - 1) % 4
        else:
            turn_index = (turn_index + 1) % 4
        step = turns[turn_index]
        position = (position[0] + step[0], position[1] + step[1])
    state["inputs"].append(grid[position])


x_min = min(grid.keys(), key = lambda t: t[0])[0]
x_max = max(grid.keys(), key = lambda t: t[0])[0]
y_min = min(grid.keys(), key = lambda t: t[1])[1]
y_max = max(grid.keys(), key = lambda t: t[1])[1]

for y in range(y_min, y_max + 1):
    row = ""
    for x in range(x_min, x_max):
        row += str(grid[(x,y)])
    print(row.replace("0", " "))