from collections import defaultdict

def get_addr(mem, pc, instr, index, rel_base):
    if len(instr) > index + 1:
        if instr[-2 - index] == "1":
            return pc + index
        elif instr[-2 - index] == "2":
            return mem[pc + index] + rel_base
    # mode = 0/position
    return mem[pc + index]

def runProg(state):
    if state["done"]: return []
    pc = state["pc"]
    mem = state["mem"]
    outputs = []
    base = 0

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
    return outputs

mem = defaultdict(int)
with open("input9") as f:
    prog = [int(x) for x in f.read().strip().split(",")]
    for i in range(len(prog)):
        mem[i] = prog[i]

state = {"nr": 0, "pc": 0, "inputs": [1], "mem": mem.copy(), "done": False}
result = runProg(state)
print(result[0])

state = {"nr": 1, "pc": 0, "inputs": [2], "mem": mem, "done": False}
result = runProg(state)
print(result[0])