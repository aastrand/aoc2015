#!/usr/bin/env python3

import json
import sys


def add(i, ignore_red=False):
    s = 0
    if type(i) == dict:
        subsum = 0
        for k, v in i.items():
            if ignore_red and v == 'red':
                subsum = 0
                break
            subsum += add(v, ignore_red=ignore_red)
        s += subsum
    elif type(i) == list:
        for e in i:
            s += add(e, ignore_red=ignore_red)
    elif type(i) == int:
        s += i

    return s


def parse(f):
    for l in open(f, 'r'):
        return json.loads(l)


def main(f):
    d = parse(f)
    print(add(d))
    print(add(d, ignore_red=True))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
