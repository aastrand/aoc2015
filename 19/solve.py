#!/usr/bin/env python3

import re
import sys
from collections import defaultdict


def parse(f):
    m = defaultdict(list)
    for l in open(f, 'r'):
        combo = l.strip().split(' => ')
        m[combo[0]].append(combo[1])
    return m


def find_distinct_replacements(mol, replacements):
    distinct = set()
    for start, replacements in replacements.items():
        for replacement in replacements:
            for pos in re.finditer(start, mol):
                pos = pos.start()
                new = mol[:pos] + replacement + mol[pos+len(start):]
                distinct.add(new)

    return distinct


def first_common(str1, str2):
    l = min(len(str1), len(str2))
    count = 0
    for i in range(l):
        if str1[i] == str2[i]:
            count += 1
        else:
            break
    return count


def test():
    replacements = {
        'H': ['HO', 'OH'],
        'O': ['HH']
    }
    mol = 'HOH'
    assert 4 == len(find_distinct_replacements(mol, replacements))


def main(f):
    test()

    replacements = parse(f)
    mol = 'ORnPBPMgArCaCaCaSiThCaCaSiThCaCaPBSiRnFArRnFArCaCaSiThCaCaSiThCaCaCaCaCaCaSiRnFYFArSiRnMgArCaSiRnPTiTiBFYPBFArSiRnCaSiRnTiRnFArSiAlArPTiBPTiRnCaSiAlArCaPTiTiBPMgYFArPTiRnFArSiRnCaCaFArRnCaFArCaSiRnSiRnMgArFYCaSiRnMgArCaCaSiThPRnFArPBCaSiRnMgArCaCaSiThCaSiRnTiMgArFArSiThSiThCaCaSiRnMgArCaCaSiRnFArTiBPTiRnCaSiAlArCaPTiRnFArPBPBCaCaSiThCaPBSiThPRnFArSiThCaSiThCaSiThCaPTiBSiRnFYFArCaCaPRnFArPBCaCaPBSiRnTiRnFArCaPRnFArSiRnCaCaCaSiThCaRnCaFArYCaSiRnFArBCaCaCaSiThFArPBFArCaSiRnFArRnCaCaCaFArSiRnFArTiRnPMgArF'

    # tried a greedy approach of replacing the longest replacement with its start
    # alas, this does not work for all inputs
    # => look at reddit for hints
    # :/

    # All of the rules are of one of the following forms:
    # α => βγ
    # α => βRnγAr
    # α => βRnγYδAr
    # α => βRnγYδYεAr

    num_symbols = 0
    num_y = 0
    for d in mol:
        if d.isupper():
            num_symbols += 1
        if d == 'Y':
            num_y += 1
    num_rn = 0
    num_ar = 0
    for n in range(0, len(mol)-1):
        sym = mol[n:n+2]
        if sym == 'Rn':
            num_rn += 1
        if sym == 'Ar':
            num_ar += 1

    print(num_symbols - num_rn - num_ar - 2*num_y - 1)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
