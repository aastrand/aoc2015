#!/usr/bin/env python3

import sys


def main(f):
    props = {}
    for l in open('props.txt', 'r'):
        prop = l.strip().split(': ')
        props[prop[0].strip()] = prop[1].strip()

    for l in open(f, 'r'):
        sue = l.split(":")[0][4:]
        offset = "Sue " + sue + ": "
        properties = [p.strip().split(': ') for p in l.strip()[len(offset):].split(',')]

        if properties[0][1] == props[properties[0][0]] and \
            properties[1][1] == props[properties[1][0]] and \
            properties[2][1] == props[properties[2][0]]:
            print(sue)

        found = True
        for prop in properties:
            if prop[0] in ('trees', 'cats'):
                found = found & (prop[1] > props[prop[0]])
            elif prop[0] in ('pomeranians', 'goldfish'):
                found = found & (prop[1] < props[prop[0]])
            else:
                found = found & (prop[1] == props[prop[0]])

        if found:
            print(sue)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
