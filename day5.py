def get_param(mem, pc, instr, index):
    if len(instr) > index + 1 and instr[-2 - index] == "1":
        return mem[pc + index]
    else: # mode = 0/position
        return mem[mem[pc + index]]

def runProg(mem, param):
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
            mem[mem[pc + 1]] = param
            pc += 2
        elif op == "4":
            print(get_param(mem, pc, instr, 1))
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

with open("input5") as f:
    prog = [int(x) for x in f.read().strip().split(",")]
runProg(prog.copy(), 1)
runProg(prog.copy(), 5)