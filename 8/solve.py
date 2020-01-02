#!/usr/bin/env python3

import sys


def main(f):
    chars = 0
    memory = 0
    encoded = 0
    for l in open(f, 'r'):
        l = l.strip()

        chars += len(l)

        ld = l.encode('utf-8').decode('unicode_escape')
        memory += len(ld) - 2

        le = l.replace('\\', '\\\\')
        le = le.replace('"', '\\"')
        encoded += len(le) + 2
    print(chars, memory, encoded, chars - memory, encoded - chars)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
