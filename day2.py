def runProg(mem):
    pc = 0
    while True:
        if mem[pc] == 1:
            mem[mem[pc+3]] = mem[mem[pc+1]] + mem[mem[pc+2]]
        elif mem[pc] == 2:
            mem[mem[pc+3]] = mem[mem[pc+1]] * mem[mem[pc+2]]
        elif mem[pc] == 99:
            break
        else:
            print(f"Unknown command {mem[pc]:d}")
        pc += 4
    return mem[0]

def part2(goal, prog):
    for noun in range(100):
        for verb in range(100):
            mem1 = prog.copy()
            mem1[1] = noun
            mem1[2] = verb
            if runProg(mem1) == goal:
                return 100 * noun + verb


with open("input2") as f:
    prog = [int(x) for x in f.read().strip().split(",")]
mem1 = prog.copy()
mem1[1] = 12
mem1[2] = 2
print(runProg(mem1))

print(part2(19690720, prog))