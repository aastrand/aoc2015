#!/usr/bin/env python3

import re
import sys


def operate(grid, op, pos1, pos2):
    for y in range(pos1[1], pos2[1]+1):
        for x in range(pos1[0], pos2[0]+1):
            op(grid, (x, y))


def turn_on(grid, pos1, pos2, part2=False):
    if part2:
        def op(grid, pos):
            value = grid.get(pos, 0)
            grid[pos] = value + 1
    else:
        def op(grid, pos):
            grid[pos] = 1

    operate(grid, op, pos1, pos2)


def turn_off(grid, pos1, pos2, part2=False):
    if part2:
        def op(grid, pos):
            value = grid.get(pos, 0)
            grid[pos] = max(0, value - 1)
    else:
        def op(grid, pos):
            grid[pos] = 0

    operate(grid, op, pos1, pos2)


def toggle(grid, pos1, pos2, part2=False):
    if part2:
        def op(grid, pos):
            value = grid.get(pos, 0)
            grid[pos] = value + 2
    else:
        def op(grid, pos):
            value = grid.get(pos, 0)
            value += 1
            grid[pos] = value % 2
    operate(grid, op, pos1, pos2)


TURN_ON = re.compile(r'^turn on ([0-9]+,[0-9]+) through ([0-9]+,[0-9]+)$')
TURN_OFF = re.compile(r'^turn off ([0-9]+,[0-9]+) through ([0-9]+,[0-9]+)$')
TOGGLE = re.compile(r'^toggle ([0-9]+,[0-9]+) through ([0-9]+,[0-9]+)$')
REGEX = {
    TURN_ON: turn_on,
    TURN_OFF: turn_off,
    TOGGLE: toggle,
}


def parse(f, part2=False):
    grid = {}

    for l in open(f, 'r'):
        for ex, fun in REGEX.items():
            m = ex.match(l.strip())
            if m:
                fun(grid, [int(p) for p in m.group(1).split(',')],
                    [int(p) for p in m.group(2).split(',')], part2)

    return grid


def sum_grid(grid):
    sum = 0
    for pos, v in grid.items():
        sum += v
    return sum


def test():
    grid = {}
    turn_on(grid, (0, 0), (999, 999))
    assert 1000000 == sum_grid(grid)
    toggle(grid, (0, 0), (999, 0))
    assert 999000 == sum_grid(grid)
    turn_off(grid, (499, 499), (500, 500))
    assert 998996 == sum_grid(grid)

    grid = {}
    turn_on(grid, (0, 0), (999, 0))
    assert 1000 == sum_grid(grid)


def main(f):
    test()

    grid = parse(f)
    print(sum_grid(grid))

    grid = parse(f, part2=True)
    print(sum_grid(grid))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
