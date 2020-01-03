#!/usr/bin/env python3

import sys
from collections import defaultdict


def has_double_pair(str):
    paircount = defaultdict(int)
    for i in range(0, len(str)-1):
        if str[i] == str[i+1]:
            paircount[str[i]+str[i+1]] += 1
    return len(paircount.keys()) > 1


def has_triple_inc(str):
    for i in range(0, len(str)-2):
        if ord(str[i]) + 2 == ord(str[i+1]) + 1 == ord(str[i+2]):
            return True

    return False


def is_valid_pw(str):
    s = set(str)
    if 'o' in s:
        return False
    if 'l' in s:
        return False
    if 'i' in s:
        return False

    return has_double_pair(str) and has_triple_inc(str)


def bump(str, pos):
    if abs(pos) > len(str):
        str.insert(0, 'a')
        return str

    c = ord(str[pos]) + 1
    if c > 122:
        str[pos] = 'a'
        return bump(str, pos - 1)
    else:
        str[pos] = chr(c)
        return str


def increment(str):
    return ''.join(bump(list(str), -1))


def test():
    assert "abcdffba" == increment("abcdffaz")
    assert "aaaaa" == increment("zzzz")

    assert False == has_double_pair("aalolen")
    assert True == has_double_pair("aalolenff")

    assert False == has_triple_inc("abdlol")
    assert True == has_triple_inc("abclol")

    assert False == is_valid_pw("hijklmmn")
    assert False == is_valid_pw("abbceffg")
    assert False == is_valid_pw("abbcegjk")


def main():
    test()

    start = "vzbxkghb"
    while not is_valid_pw(start):
        start = increment(start)
    print(start)

    start = increment(start)
    while not is_valid_pw(start):
        start = increment(start)
    print(start)


if __name__ == '__main__':
    sys.exit(main())
