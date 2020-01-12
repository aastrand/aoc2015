#!/usr/bin/env python3

import sys
from collections import defaultdict
from itertools import combinations


def main(f):
    containers = [int(l.strip()) for l in open(f, 'r')]
    liters = 150

    count = 0
    lengths = defaultdict(int)
    for p in range(2, len(containers)):
        for c in combinations(containers, p):
            if sum(c) == liters:
                count += 1
                lengths[len(c)] += 1

    print(count)
    min_val = min(lengths.keys())
    print(lengths[min_val])


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
