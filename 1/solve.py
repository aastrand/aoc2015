#!/usr/bin/env python3

import sys


def main(f):
    sum = 0
    basement = False
    for l in open(f, 'r'):
        for i, d in enumerate(l, start=1):
            sum += 1 if d == '(' else -1
            if sum < 0 and not basement:
                basement = True
                print('basement', i)

    print(sum)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
