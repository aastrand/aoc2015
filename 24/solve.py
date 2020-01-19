#!/usr/bin/env python3

import sys
from functools import reduce


def product(l):
    return reduce((lambda x, y: x * y), l)


def main(f):
    # manually try and add up groups, using the largest and working backwards
    # while trying to get as few sizes as possible

    total_sum = 0
    for l in open(f, 'r'):
        n = int(l.strip())
        total_sum += n

    # part 1
    balanced = total_sum // 3

    # we know that sum of a group == 512
    # try to add the largest numbers together to form 512 and see what the QE looks like.

    # here we get one group with 1, which lowers the QE
    guess = [113, 109, 107, 103, 79, 1]
    assert balanced == sum(guess)
    print(product(guess))

    # part 2
    balanced = total_sum // 4

    # same guesswork
    # here we get a group of length 4
    guess = [113, 109, 103, 59]
    assert balanced == sum(guess)
    print(product(guess))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
