#!/usr/bin/env python3

import re
import sys
from collections import defaultdict


def run_reindeer(speed, time, resting_time, run_time):
    total = time + resting_time
    laps = run_time // total
    rest = run_time - (laps * total)

    return laps * time * speed + (speed * (rest if rest < time else time))


def race(reindeer, run_time):
    max_distance = 0
    animal = None
    for r in reindeer:
        distance = run_reindeer(r[1], r[2], r[3], run_time)
        if distance > max_distance:
            max_distance = distance
            animal = r[0]
    return animal, max_distance


# Vixen can fly 8 km/s for 8 seconds, but then must rest for 53 seconds.
RACE_RE = re.compile('^([A-Za-z]+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.$')
def parse(f):
    reindeer = []
    for l in open(f, 'r'):
        m = RACE_RE.match(l.strip())
        if m:
            reindeer.append((m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))))

    return reindeer


def test():
    assert 1120 == run_reindeer(14, 10, 127, 1000)
    assert 1056 == run_reindeer(16, 11, 162, 1000)


def main(f):
    test()

    reindeer = parse(f)
    print(race(reindeer, 2503))

    score_map = defaultdict(int)
    for s in range(2504):
        animal, distance = race(reindeer, s)
        score_map[animal] += 1

    print(score_map)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
