#!/usr/bin/env python3

import sys


def main(f):
    paper = 0
    ribbon = 0
    for l in open(f, 'r'):
        parts = l.split('x')
        parts = [int(p) for p in parts]
        sides = [parts[0] * parts[1], parts[1] * parts[2], parts[2]*parts[0]]

        paper += sum(sides)*2 + min(sides)

        parts = sorted(parts)
        ribbon += parts[0] + parts[0] + parts[1] + parts[1] + (parts[0] * parts[1] * parts[2])

    print(paper)
    print(ribbon)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
