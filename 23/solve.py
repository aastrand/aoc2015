#!/usr/bin/env python3

import sys


# hlf r sets register r to half its current value, then continues with the next instruction.
def hlf(program, pc, registers):
    registers[program[pc][1]] /= 2
    return pc + 1


# tpl r sets register r to triple its current value, then continues with the next instruction.
def tpl(program, pc, registers):
    registers[program[pc][1]] *= 3
    return pc + 1


# inc r increments register r, adding 1 to it, then continues with the next instruction.
def inc(program, pc, registers):
    registers[program[pc][1]] += 1
    return pc + 1


# jmp offset is a jump; it continues with the instruction offset away relative to itself.
def jmp(program, pc, registers):
    return pc + program[pc][1]


# jio r, offset is like jmp, but only jumps if register r is 1 ("jump if one", not odd).
def jio(program, pc, registers):
    if registers[program[pc][1]] == 1:
        return pc + program[pc][2]
    return pc + 1


# jie r, offset is like jmp, but only jumps if register r is even ("jump if even").
def jie(program, pc, registers):
    if registers[program[pc][1]] % 2 == 0:
        return pc + program[pc][2]
    return pc + 1


OP_MAP = {
    'hlf': hlf,
    'tpl': tpl,
    'inc': inc,
    'jmp': jmp,
    'jio': jio,
    'jie': jie
}


def run(program, a=0, b=0):
    registers = {'a': a, 'b': b}
    pc = 0

    while -1 < pc < len(program):
        op = program[pc]
        pc = OP_MAP[op[0]](program, pc, registers)

    print(registers)


def parse(f):
    program = []
    for l in open(f, 'r'):
        op = tuple(l.strip().split(' '))
        if op[0] in ('jio', 'jie'):
            program.append((op[0], op[1][:1], int(op[2])))
        elif op[0] == 'jmp':
            program.append((op[0], int(op[1])))
        else:
            program.append(op)

    return program


def main(f):
    program = parse(f)
    run(program)
    run(program, a=1)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
