#!/usr/bin/env python3

import sys
from itertools import permutations


def parse(f):
    lookup = {}
    for l in open(f, 'r'):
        l = l.strip()
        parts = l.split('=')
        dist = int(parts[1].strip())
        cities = parts[0].strip().split(' to ')
        lookup[(cities[0], cities[1])] = dist
        lookup[(cities[1], cities[0])] = dist

    return lookup


def distance(distances, cities):
    dist = 0
    for i in range(len(cities) - 1):
        dist += distances[(cities[i], cities[i+1])]
    return dist


def main(f):
    distances = parse(f)
    cities = set([p[0] for p in distances.keys()])

    min = float('inf')
    max = float('-inf')
    min_route = None
    for perm in permutations(cities):
        dist = distance(distances, perm)
        if dist < min:
            min = dist
            min_route = perm
        if dist > max:
            max = dist
            max_route = perm
    print(min, min_route)
    print(max, max_route)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
