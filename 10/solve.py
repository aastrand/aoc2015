#!/usr/bin/env python3

import sys


def lns(n):
    r = []
    last = None
    num = 1
    for d in str(n):
        if d == last:
            num += 1
        elif last is not None:
            r.append(str(num))
            r.append(last)
            num = 1
        last = d


    r.append(str(num))
    r.append(last)
    return ''.join(r)


def test():
    assert "11" == lns(1)
    assert "21" == lns(11)
    assert "1211" == lns(21)
    assert "111221" == lns(1211)
    assert "312211" == lns(111221)


def main():
    test()

    s = "1113122113"
    for _ in range(40):
        s = lns(s)
    print(len(s))

    s = "1113122113"
    for _ in range(50):
        s = lns(s)
    print(len(s))


if __name__ == '__main__':
    sys.exit(main())
