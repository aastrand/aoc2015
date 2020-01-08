#!/usr/bin/env python3

import re
import sys
from itertools import permutations


HAPPY_RE = re.compile('^([A-Za-z]+) would (gain|lose) (\d+) happiness units by sitting next to ([A-Za-z]+).$')
def parse(f):
    happy_map = {}
    for l in open(f, 'r'):
        m = HAPPY_RE.match(l.strip())
        if m:
            happy_map[(m.group(1), m.group(4))] = int(m.group(3)) * (1 if m.group(2) == 'gain' else -1)

    return happy_map


def get_max_seating(happy_map, people):
    max_sum = 0
    max_people = None

    for perm in permutations(people):
        sum = 0
        for i in range(-1, len(perm) - 1):
            sum += happy_map[(perm[i], perm[i+1])]
            sum += happy_map[(perm[i+1], perm[i])]

        if sum > max_sum:
            max_sum = sum
            max_people = people

    return max_sum, max_people


def main(f):
    happy_map = parse(f)
    people = set([k[0] for k in happy_map.keys()])

    print(get_max_seating(happy_map, people))

    for person in people:
        happy_map[('you', person)] = 0
        happy_map[(person, 'you')] = 0
    people.add('you')

    print(get_max_seating(happy_map, people))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
