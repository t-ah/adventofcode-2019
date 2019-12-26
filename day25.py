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

mem = parse("input25")
state = create_state("", mem.copy())

while not state["done"]:
    run_prog(state, True)
    state["inputs"] = [ord(x) for x in input()] + [10]
    # playing games is for human people