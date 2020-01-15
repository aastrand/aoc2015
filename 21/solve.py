#!/usr/bin/env python3

import sys
from itertools import combinations


class Character:

    def __init__(self, name, hp, dmg, ac):
        self.name = name
        self.hp = hp
        self._dmg = dmg
        self._ac = ac
        self._items = []

    def dmg(self):
        return sum([item.dmg for item in self._items]) + self._dmg

    def ac(self):
        return sum([item.ac for item in self._items]) + self._ac

    def attack(self, char, verbose=False):
        dmg = max(1, self.dmg() - char.ac())
        if verbose:
            print(self.name, "deals", dmg, "to", char.name)
        char.hp -= dmg
        if verbose and not char.alive():
            print(char.name, "dies")

    def equip(self, item):
        self._items.append(item)

    def alive(self):
        return self.hp > 0


class Item:

    def __init__(self, name, cost, dmg, ac):
        self.name = name
        self.cost = cost
        self.dmg = dmg
        self.ac = ac

    def __str__(self):
        return self.name + ": " + "cost: " + str(self.cost) + "g, dmg: " + str(self.dmg) + ", ac: " + str(self.ac)

    def __repr__(self):
        #return {"name": self.name, "cost": self.cost, "dmg": self.dmg, "ac": self.ac}
        return self.__str__()


def fight(c1, c2):
    while (c1.hp > 0 and c2.hp > 0):
        c1.attack(c2)
        if c2.alive():
            c2.attack(c1)


def test():
    # For example, suppose you have 8 hit points, 5 damage, and 5 armor, and that the boss has 12 hit points, 7 damage, and 2 armor:
    #
    # The player deals 5-2 = 3 damage; the boss goes down to 9 hit points.
    # The boss deals 7-5 = 2 damage; the player goes down to 6 hit points.
    # The player deals 5-2 = 3 damage; the boss goes down to 6 hit points.
    # The boss deals 7-5 = 2 damage; the player goes down to 4 hit points.
    # The player deals 5-2 = 3 damage; the boss goes down to 3 hit points.
    # The boss deals 7-5 = 2 damage; the player goes down to 2 hit points.
    # The player deals 5-2 = 3 damage; the boss goes down to 0 hit points.
    you = Character("player", 8, 5, 5)
    boss = Character("boss", 12, 7, 2)
    fight(you, boss)
    assert you.alive()
    assert not boss.alive()


# Weapons:    Cost  Damage  Armor
# Dagger        8     4       0
# Shortsword   10     5       0
# Warhammer    25     6       0
# Longsword    40     7       0
# Greataxe     74     8       0
WEAPONS = [
    Item("Dagger",        8,     4,       0),
    Item("Shortsword",   10,     5,       0),
    Item("Warhammer",    25,     6,       0),
    Item("Longsword",    40,     7,       0),
    Item("Greataxe",     74,     8,       0)
]


# Armor:      Cost  Damage  Armor AC/g
# Leather      13     0       1
# Chainmail    31     0       2
# Splintmail   53     0       3
# Bandedmail   75     0       4
# Platemail   102     0       5
ARMOR = [
    Item("Leather",      13,     0,       1),
    Item("Chainmail",    31,     0,       2),
    Item("Splintmail",   53,     0,       3),
    Item("Bandedmail",   75,     0,       4),
    Item("Platemail",   102,     0,       5)
]


# Rings:      Cost  Damage  Armor
# Damage +1    25     1       0
# Damage +2    50     2       0
# Damage +3   100     3       0
# Defense +1   20     0       1
# Defense +2   40     0       2
# Defense +3   80     0       3
RINGS = [
    Item("Damage +1",    25,     1,       0),
    Item("Damage +2",    50,     2,       0),
    Item("Damage +3",   100,     3,       0),
    Item("Defense +1",   20,     0,       1),
    Item("Defense +2",   40,     0,       2),
    Item("Defense +3",   80,     0,       3)
]


def item_combos_least_gold():
    # exactly 1 weapon, armor optional

    # manual guess
    # 40 + 31 + 20 = 91
    yield (WEAPONS[3], ARMOR[1], RINGS[3])


def item_combos_most_gold():
    # bruteforce
    optionals = ARMOR + RINGS
    for weapon in WEAPONS:
        for size in range(1, len(optionals) + 1):
            for c in combinations(optionals, size):
                combo = [weapon]
                combo.extend(c)
                yield combo


def main():
    test()

    # Player
    # Damage: 0
    # Armor: 0

    # Boss
    # Hit Points: 100
    # Damage: 8
    # Armor: 2

    for items in item_combos_least_gold():
        player = Character("player", 100, 0, 0)
        boss = Character("boss", 100, 8, 2)

        for i in items:
            player.equip(i)
        print(sum([i.cost for i in player._items]), player._items)
        fight(player, boss)

    combos = []
    for items in item_combos_most_gold():
        player = Character("player", 100, 0, 0)
        boss = Character("boss", 100, 8, 2)

        for i in items:
            player.equip(i)
        fight(player, boss)
        if not player.alive():
            combos.append(items)

    max_gold = 0
    items = None
    for combo in combos:
        cost = sum([i.cost for i in combo])
        if cost > max_gold:
            max_gold = cost
            items = combo
    print(max_gold, items)

if __name__ == '__main__':
    sys.exit(main())
