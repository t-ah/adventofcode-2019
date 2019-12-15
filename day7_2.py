import itertools

def get_param(mem, pc, instr, index):
    if len(instr) > index + 1 and instr[-2 - index] == "1":
        return mem[pc + index]
    else: # mode = 0/position
        return mem[mem[pc + index]]

def runProg(state):
    if state["done"]:
        return []
    pc = state["pc"]
    mem = state["mem"]
    outputs = []

    while True:
        instr = str(mem[pc])
        op = instr[-1]
        if op == "1":
            mem[mem[pc+3]] = get_param(mem, pc, instr, 1) + get_param(mem, pc, instr, 2)
            pc += 4
        elif op == "2":
            mem[mem[pc+3]] = get_param(mem, pc, instr, 1) * get_param(mem, pc, instr, 2)
            pc += 4
        elif op == "3":
            if len(state["inputs"]) > 0:
                mem[mem[pc + 1]] = state["inputs"].pop(0)
                pc += 2
            else: # wait for new inputs
                break
        elif op == "4":
            output = get_param(mem, pc, instr, 1)
            outputs.append(output)
            pc += 2
        elif op == "5":
            if get_param(mem, pc, instr, 1) != 0:
                pc = get_param(mem, pc, instr, 2)
            else:
                pc += 3
        elif op == "6":
            if get_param(mem, pc, instr, 1) == 0:
                pc = get_param(mem, pc, instr, 2)
            else:
                pc += 3
        elif op == "7":
            v = 0
            if get_param(mem, pc, instr, 1) < get_param(mem, pc, instr, 2):
                v = 1
            mem[mem[pc + 3]] = v
            pc += 4
        elif op == "8":
            v = 0
            if get_param(mem, pc, instr, 1) == get_param(mem, pc, instr, 2):
                v = 1
            mem[mem[pc + 3]] = v
            pc += 4
        elif op == "9":
            state["done"] = True
            break
        else:
            print(f"Unknown command {mem[pc]:d}")
            break
    state["pc"] = pc
    return outputs

with open("input7") as f:
    prog = [int(x) for x in f.read().strip().split(",")]

results = []
for perm in itertools.permutations(range(5,10)):
    states = []
    for i in range(5):
        states.append({"nr": i, "pc": 0, "inputs": [perm[i]], "mem": prog.copy(), "done": False})
    states[0]["inputs"].append(0) # 0 is first input to A - NO IT'S NOT!!! IT'S THE 2ND!! ARGH
    state_index = 0
    inst_results = []
    while True:
        outputs = runProg(states[state_index])
        if state_index == 4:
            inst_results += outputs
            if states[4]["done"]:
                break
        state_index = (state_index + 1) % 5
        states[state_index]["inputs"] += outputs
    results.append(inst_results[-1])
print(max(results))
