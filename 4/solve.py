#!/usr/bin/env python3

import hashlib
import sys


def hash(msg):
    m = hashlib.md5()
    m.update(msg.encode('utf-8'))
    return m.hexdigest()


def test():
    print(hash('abcdef' + '609043'))
    print(hash('pqrstuv' + '1048970'))


def main():
    test()

    secret = 'iwrupvqb'
    i = 1
    found = False
    while True:
        if not found and hash(secret+str(i))[:5] == '00000':
            print(i)
            found = True

        if hash(secret+str(i))[:6] == '000000':
            print(i)
            break
        i += 1


if __name__ == '__main__':
    sys.exit(main())
