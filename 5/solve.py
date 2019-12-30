#!/usr/bin/env python3

import sys
from collections import defaultdict


def is_nice(str):
    forbidden = set(['ab', 'cd', 'pq', 'xy'])
    vowels = set(['a', 'e', 'i', 'o', 'u'])

    vowel_count = 0
    double = False
    is_forbidden = False
    last = None

    for d in str.strip():
        if last is not None:
            substr  = last+d
            if substr in forbidden:
                is_forbidden = True
                break

            if last == d:
                double = True

        if d in vowels:
            vowel_count += 1

        last = d

    return vowel_count > 2 and double and not is_forbidden


def is_nice2(str):
    repeat = False
    double = False
    pairs = defaultdict(list)
    paircount = defaultdict(int)

    for i in range(0, len(str)-1):
        pair = str[i]+str[i+1]
        paircount[pair] += 1
        for idx in pairs.get(pair, []):
            if idx is not None and abs(idx-i) > 1:
                double = True
        pairs[pair].append(i)
        if i < len(str) - 2:
            if str[i] == str[i+2]:
                repeat = True

    return double and repeat


def test():
    assert True == is_nice('ugknbfddgicrmopn')
    assert True == is_nice('aaa')
    assert False == is_nice('jchzalrnumimnmhp')
    assert False == is_nice('haegwjzuvuyypxyu')
    assert False == is_nice('dvszwmarrgswjxmb')

    assert True == is_nice2('qjhvhtzxzqqjkmpb')
    assert True == is_nice2('xxyxx')
    assert True == is_nice2('abcdeeeghiab')
    assert True == is_nice2('aaadedaa')
    assert False == is_nice2('aaa')
    assert False == is_nice2('uurcxstgmygtbstg')
    assert False == is_nice2('ieodomkazucvgmuy')
    assert True == is_nice2('xilodxfuxphuiiii')

def main(f):
    test()

    count = 0
    count2 = 0

    for l in open(f, 'r'):
        if is_nice(l.strip()):
            count += 1
        if is_nice2(l.strip()):
            count2 += 1

    print(count)
    print(count2)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
