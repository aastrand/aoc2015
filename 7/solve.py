#!/usr/bin/env python3

import sys


def try_cast(str):
    try:
        return int(str)
    except ValueError:
        return None


def rshift(a, b):
    return a >> b


def lshift(a, b):
    return a << b


def _and(a, b):
    return a & b


def _or(a, b):
    return a | b


def _not(a):
    return 65535 - a


OPS = {
    'OR': _or,
    'AND': _and,
    'LSHIFT': lshift,
    'RSHIFT': rshift
}


def parse(f):
    grid = {}

    for l in open(f, 'r'):
        op, wire = l.strip().split('->')
        wire = wire.strip()
        op = op.strip()

        num = try_cast(op)
        if num is None:
            grid[wire] = op.split(' ')
        else:
            grid[wire] = [num]

    return grid

CACHE = {}
def fetch(grid, wire):
    cached = CACHE.get(wire)
    if cached is not None:
        return cached

    num = try_cast(wire)
    if num is not None:
        r = [num]
    else:
        vals = grid[wire]
        if len(vals) == 1:
            num = try_cast(vals[0])
            if num is None:
                r =  [fetch(grid, vals[0])]
            else:
                r = [num]
        elif len(vals) == 2:
            r = [_not(fetch(grid, vals[1])[0])]
        else:
            fun = OPS[vals[1]]
            r = [fun(fetch(grid, vals[0])[0], fetch(grid, vals[2])[0])]

    CACHE[wire] = r
    return r


def solve(grid):
    solved = {}
    for wire in grid.keys():
        val = fetch(grid, wire)
        solved[wire] = val

    return solved


def main(f):
    grid = parse(f)
    grid = solve(grid)
    print(grid['a'])

    grid = parse(f)
    grid['b'] = ['956']
    CACHE.clear()
    grid = solve(grid)
    print(grid['a'])


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
