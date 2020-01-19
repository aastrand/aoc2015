#!/usr/bin/env python3

import sys


def value_at(n):
    base = 20151125
    mul = 252533
    div = 33554393

    val = base
    for _ in range(1, n):
        val = val * mul % div

    return val


def power_at_pos(x, y):
    pow = 0
    for i in range(1, x+1):
        pow += i

    for i in range(x, x+y-1):
        pow += i

    return pow


def test():
    #    |  1   2   3   4   5   6
    # ---+---+---+---+---+---+---+
    #  1 |  1   3   6  10  15  21
    #  2 |  2   5   9  14  20
    #  3 |  4   8  13  19
    #  4 |  7  12  18
    #  5 | 11  17
    #  6 | 16

    assert 20 == power_at_pos(5, 2)
    assert 19 == power_at_pos(4, 3)
    assert 18 == power_at_pos(3, 4)

    # |    1         2         3         4         5         6
    # ---+---------+---------+---------+---------+---------+---------+
    #  1 | 20151125  18749137  17289845  30943339  10071777  33511524
    #  2 | 31916031  21629792  16929656   7726640  15514188   4041754
    #  3 | 16080970   8057251   1601130   7981243  11661866  16474243
    #  4 | 24592653  32451966  21345942   9380097  10600672  31527494
    #  5 |    77061  17552253  28094349   6899651   9250759  31663883
    #  6 | 33071741   6796745  25397450  24659492   1534922  2799500

    assert 20151125 == value_at(1)
    assert 33071741 == value_at(16)
    assert 33511524 == value_at(21)

    assert 21345942 == value_at(power_at_pos(3, 4))


def main():
    test()

    # To continue, please consult the code grid in the manual.  Enter the code at row 2981, column 3075.
    print(value_at(power_at_pos(3075, 2981)))


if __name__ == '__main__':
    sys.exit(main())
