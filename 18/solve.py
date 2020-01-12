#!/usr/bin/env python3

import sys


def parse(f):
    grid = {}
    y = 0
    for l in open(f, 'r'):
        x = 0
        for d in l.strip():
            grid[(x, y)] = d
            x += 1
        y += 1

    return grid


def offset_pos(pos, offset):
    return (pos[0]+offset[0], pos[1]+offset[1])


OFFSETS = [
    (0, 1),
    (1, 0),
    (-1, 0),
    (0, -1),
    (1, 1),
    (-1, -1),
    (1, -1),
    (-1, 1)
]
def count_neighbours_on(grid, pos):
    count = 0
    for offset in OFFSETS:
        if grid.get(offset_pos(pos, offset)) == '#':
            count += 1
    return count


def turn_on_edges(grid, size):
    grid[(0, 0)] = '#'
    grid[(0, size)] = '#'
    grid[(size, 0)] = '#'
    grid[(size, size)] = '#'


def evolve(grid, size = 99, stuck = False):
    new_grid = {}
    for pos in grid.keys():
        count = count_neighbours_on(grid, pos)
        val = grid[pos]

        if val == '#':
            if count == 2 or count == 3:
                new_grid[pos] = '#'
            else:
                new_grid[pos] = '.'
        else:
            if count == 3:
                new_grid[pos] = '#'
            else:
                new_grid[pos] = '.'

    if stuck:
        turn_on_edges(new_grid, size)

    return new_grid


def print_grid(grid, size = None):
    max_x = size or max([p[0] for p in grid.keys()])
    max_y = size or max([p[1] for p in grid.keys()])
    for y in range(0, max_y + 1):
        for x in range(0, max_x + 1):
            print(grid[(x, y)], end='')
        print()


def count_on(grid):
    count = 0
    for v in grid.values():
        if v == '#':
            count += 1
    return count


def test():
    grid = parse('example.txt')
    for _ in range(5):
        print_grid(grid)
        print()
        grid = evolve(grid)
    assert count_on(grid) == 4

    grid = parse('example.txt')
    turn_on_edges(grid, 5)
    for _ in range(5):
        print_grid(grid, 5)
        print()
        grid = evolve(grid, 5, True)
    assert count_on(grid) == 17


def main(f):
    test()

    grid = parse(f)
    for _ in range(100):
        grid = evolve(grid)
    print(count_on(grid))

    grid = parse(f)
    turn_on_edges(grid, 99)
    for _ in range(100):
        grid = evolve(grid, 99, True)
    print(count_on(grid))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
