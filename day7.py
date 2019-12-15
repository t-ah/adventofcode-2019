import itertools

def get_param(mem, pc, instr, index):
    if len(instr) > index + 1 and instr[-2 - index] == "1":
        return mem[pc + index]
    else: # mode = 0/position
        return mem[mem[pc + index]]

def runProg(mem, params):
    pc = 0
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
            mem[mem[pc + 1]] = params.pop(0)
            pc += 2
        elif op == "4":
            output = get_param(mem, pc, instr, 1)
            #print("out:", output)
            params.insert(1, output)
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
            break
        else:
            print(f"Unknown command {mem[pc]:d}")
            break
    return

with open("input7") as f:
    prog = [int(x) for x in f.read().strip().split(",")]

results = []
for perm in itertools.permutations(range(5)):
    phases = list(perm[:1] + (0,) + perm[1:])
    for _ in range(5):
        runProg(prog.copy(), phases)
    results.append(phases[0])
print(max(results))