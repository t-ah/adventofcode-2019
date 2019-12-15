from collections import defaultdict, deque
import copy

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

def run_prog(state):
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

def step(state, direction):
    state["inputs"] += [direction]
    outputs = run_prog(state)
    return outputs[0]

mem = parse("input15")
path_lengths = {(0,0): 0}
states = {(0,0): create_state("", mem.copy())}
direction = {1: (0,-1), 2: (0,1), 3: (-1,0), 4: (1,0)}

new_positions = deque()
new_positions.append((0,0))

goal = (0,0)
while len(new_positions) > 0:
    pos = new_positions.pop()
    path_length = path_lengths[pos]
    for i in range(1,5):
        state = copy.deepcopy(states[pos])
        result = step(state, i)
        new_pos = (pos[0] + direction[i][0], pos[1] + direction[i][1])
        if result == 2:
            goal = new_pos
        if result > 0:
            if new_pos in path_lengths:
                old_path_l = path_lengths[new_pos]
                if old_path_l > path_length + 1:
                    path_lengths[new_pos] = path_length + 1
                    new_positions.append(new_pos)
            else:
                path_lengths[new_pos] = path_length + 1
                new_positions.append(new_pos)
                states[new_pos] = state

print(path_lengths[goal])

# part 2

visited = set()
visited.add(goal)
new_nodes = set()
new_nodes.add(goal)
time = -1

while len(new_nodes) > 0:
    old_nodes = new_nodes
    new_nodes = set()
    time += 1
    for pos in old_nodes:
        for i in range(1,5):
            new_pos = (pos[0] + direction[i][0], pos[1] + direction[i][1])
            if new_pos in path_lengths and new_pos not in visited:
                visited.add(new_pos)
                new_nodes.add(new_pos)
print(time)