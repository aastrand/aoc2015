#!/usr/bin/env python3

import sys


MOVES = {
    '>': (1, 0),
    '<': (-1 ,0),
    '^': (0, -1),
    'v': (0, 1)
}


def offset_pos(pos, offset):
    return (pos[0]+offset[0], pos[1]+offset[1])


def main(f):
    pos = (0, 0)
    grid = {pos: ''}
    for l in open(f, 'r'):
        for dir in l.strip():
            pos = offset_pos(pos, MOVES[dir])
            grid[pos] = ''

    print(len(grid.values()))

    pos1 = (0, 0)
    pos2 = (0, 0)
    positions = [pos1, pos2]
    count = 0
    grid = {pos1: ''}
    for l in open(f, 'r'):
        for dir in l.strip():
            pos = positions[count % 2]
            pos = offset_pos(pos, MOVES[dir])
            positions[count % 2] = pos

            grid[pos] = ''
            count += 1

    print(len(grid.values()))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
