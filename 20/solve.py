#!/usr/bin/env python3

import sys
from collections import defaultdict
from math import sqrt


def divisors(n):
    divs = {1, n}
    for i in range(2, int(sqrt(n)) + 1):
        if n % i == 0:
            divs.update((i, n//i))
    return divs


def presents(n):
    sum = 0
    for d in divisors(n):
        sum += 10*d

    return sum


def presents_part2(n):
    sum = 0
    divs = sorted([d for d in divisors(n)])
    for d in divs:
        if n <= 50*d:
            sum += 11*d

    return sum


def test():
    # 1 [1] 10
    # 2 [1, 2] 30
    # 3 [1, 3] 40
    # 4 [1, 2, 4] 70
    # 5 [1, 5] 60
    # 6 [1, 2, 3, 6] 120
    # 7 [1, 7] 80
    # 8 [1, 2, 4, 8] 150
    # 9 [1, 3, 9] 130
    # 10 [1, 2, 5, 10] 180
    assert 10 == presents(1)
    assert 30 == presents(2)
    assert 40 == presents(3)
    assert 70 == presents(4)
    assert 60 == presents(5)
    assert 120 == presents(6)
    assert 80 == presents(7)
    assert 150 == presents(8)
    assert 130 == presents(9)
    assert 180 == presents(10)


def main():
    test()

    # observation: each visiting # is a divisor to the house #
    # so, presents = 10 * sum (divisors)
    n = 29000000
    h = 1000000 # starting guess
    while True:
        p = presents(h)
        if p >= n:
            print(h)
            break
        h += 1

    # here, we stop visiting after 50 visits
    # so, a house only gets a present from a divisor if its less than 50 * visitor #
    h = 1000000
    while True:
        p = presents_part2(h)
        if p >= n:
            print(h)
            break
        h += 1


if __name__ == '__main__':
    sys.exit(main())
