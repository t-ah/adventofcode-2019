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
    return {"name": name, "pc": 0, "inputs": [], "mem": mem, "done": False, "base": 0, "outputs": []}

def get_addr(mem, pc, instr, index, rel_base):
    if len(instr) > index + 1:
        if instr[-2 - index] == "1":
            return pc + index
        elif instr[-2 - index] == "2":
            return mem[pc + index] + rel_base
    return mem[pc + index]

def step(state):
    if state["done"]: return []
    pc = state["pc"]
    base = state["base"]
    mem = state["mem"]
    outputs = state["outputs"]

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
        else:
            mem[get_addr(mem, pc, instr, 1, base)] = -1
        pc += 2
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
        else:
            base += mem[get_addr(mem, pc, instr, 1, base)]
            pc += 2
    else:
        print(f"Unknown command {mem[pc]:d}")
    state["pc"] = pc
    state["base"] = base
    return outputs

mem = parse("input23")

states = []
for x in range(50):
    state = create_state(x, mem.copy())
    state["inputs"].append(x)
    states.append(state)

done = False
while not done:
    for state in states:
        outputs = step(state)
        if len(outputs) == 3:
            address = outputs[0]
            if address == 255:
                print(outputs[2])
                done = True
                break
            states[outputs[0]]["inputs"] += outputs[1:]
            state["outputs"] = []