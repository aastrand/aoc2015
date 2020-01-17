#!/usr/bin/env python3

import copy
import sys


class NotEnoughManaException(Exception):
    pass


class EffectAlreadyExistsException(Exception):
    pass


class PlayerDeadException(Exception):
    pass


class Character:

    def __init__(self, name, hp, mana, dmg, ac):
        self.name = name
        self.hp = hp
        self.mana = mana
        self._dmg = dmg
        self._ac = ac
        self._items = []
        self.mana_spent = 0

    def dmg(self):
        return sum([item.dmg for item in self._items]) + self._dmg

    def ac(self):
        return sum([item.ac for item in self._items]) + self._ac

    def attack(self, char):
        dmg = max(1, self.dmg() - char.ac())
        log(self.name, "attacks for", self.dmg(), "-", char.ac(), "=", dmg, "damage!")
        char.take_dmg(dmg)

    def use_mana(self, mana):
        if self.mana < mana:
            raise NotEnoughManaException("Tried using", mana, "mana, but only have", self.mana)

        self.mana_spent += mana
        self.mana -= mana

    def take_dmg(self, dmg):
        self.hp -= dmg
        if not self.alive():
            log(self.name, "dies")

    def equip(self, item):
        self._items.append(item)

    def alive(self):
        return self.hp > 0


class Effect:

    def __init__(self, name, turns, fun):
        self.name = name
        self.turns = turns
        self.fun = fun

    def pre(self):
        pass

    def apply(self):
        if self.active():
            self.turns -= 1
            if self.fun:
                self.fun()
            log(self.name, "timer is now", self.turns, ".")

    def destroy(self):
        log(self.name, "wears off")

    def active(self):
        return self.turns > 0


class Shield(Effect):

    def __init__(self, name, turns, fun, target):
        super(Shield, self).__init__(name, turns, fun)
        self.target = target
        self.original_ac = None

    def pre(self):
        if self.active() and not self.original_ac:
            self.original_ac = self.target._ac
            self.target._ac += 7

    def destroy(self):
        log(self.name, "wears off, decreasing armor by 7.")
        if self.original_ac is not None:
            self.target._ac = self.original_ac
            self.original_ac = None


LOGLEVEL = 'debug'
def log(*str, **kw):
    if LOGLEVEL == 'debug':
        print(*str, **kw)


# 13.25 mana / dmg
# Magic Missile costs 53 mana. It instantly does 4 damage.
def magic_missile(caster, target, cost=53):
    caster.use_mana(cost)
    target.hp -= 4
    log(caster.name, "casts Magic Missile, dealing 4 damage.")


# 18.25 mana / dmg, 18.25 mana / hp
# Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
def drain(caster, target, cost=73):
    caster.use_mana(cost)
    target.hp -= 2
    caster.hp += 2
    log(caster.name, "casts Drain, dealing 2 damage, and healing 2 hit points.")


# 42 hp for 113 mana, 2.6905 mana / hp
# Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it is active, your armor is increased by 7.
def shield(caster, cost=113):
    caster.use_mana(cost)
    log(caster.name, "casts Shield, increasing armor by 7.")
    return Shield("Shield", 6, None, caster)


# 9.6111 mana / dmg
# Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the start of each turn while it is active, it deals the boss 3 damage.
def poison(caster, target, cost=173):
    caster.use_mana(cost)
    log(caster.name, "casts Poison.")

    def fun():
        log("Poison deals 3 damage; ", end='')
        target.hp -= 3

    return Effect("Poison", 6, fun)


# gain 505 - 229 = 276 mana over 5 turns
# Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the start of each turn while it is active, it gives you 101 new mana.
def recharge(caster, cost=229):
    caster.use_mana(cost)
    log(caster.name, "casts Recharge.")

    def fun():
        log("Recharge provides 101 mana; ", end='')
        caster.mana += 101

    return Effect("Recharge", 5, fun)


def player_dies(player):
    if not player.alive():
        log("This kills the player. You lose.")
        log("<><><><><><><><><><><><><><><><>")
        log()
        return True

    return False


def boss_dies(boss):
    if not boss.alive():
        log("This kills the boss, and the player wins.")
        log("=========================================")
        log()
        return True

    return False


def turn(player, boss, boss_turn, effects, spell, hard_mode=False):
    log("--", boss.name if boss_turn else player.name, "turn --")
    log("-", player.name, "has", player.hp, "hit points,", player.ac(), "armor,", player.mana, "mana")
    log("-", boss.name, "has", boss.hp, "hit points")

    if hard_mode and not boss_turn:
        log(player.name, "takes 1 damage.")
        player.hp -= 1
        if player_dies(player):
            raise PlayerDeadException()

    # apply effects
    remaining = []
    for effect in effects:
        effect.apply()
        if effect.active():
            remaining.append(effect)
        else:
            effect.destroy()
    effects = remaining

    if boss_dies(boss):
        return None

    # action per turn
    if boss_turn:
        boss.attack(player)

        if player_dies(player):
            raise PlayerDeadException()
    else:
        effect = spell()
        if effect:
            if effect.name in [e.name for e in effects]:
                raise EffectAlreadyExistsException(effect.name, "already in effect list")

            effect.pre()
            effects.append(effect)

    if boss_dies(boss):
        return None

    log()

    return effects


def test():
    # For example, suppose the player has 10 hit points and 250 mana, and that the boss has 13 hit points and 8 damage:
    player = Character('Player', 10, 250, 0, 0)
    boss = Character('Boss', 13, 0, 8, 0)
    effects = []

    # -- Player turn --
    # - Player has 10 hit points, 0 armor, 250 mana
    # - Boss has 13 hit points
    # Player casts Poison.
    boss_turn = False
    effects = turn(player, boss, boss_turn, effects, lambda: poison(player, boss))

    # -- Boss turn --
    # - Player has 10 hit points, 0 armor, 77 mana
    # - Boss has 13 hit points
    # Poison deals 3 damage; its timer is now 5.
    # Boss attacks for 8 damage.
    boss_turn = boss_turn ^ True
    effects = turn(player, boss, boss_turn, effects, lambda: _)

    # -- Player turn --
    # - Player has 2 hit points, 0 armor, 77 mana
    # - Boss has 10 hit points
    # Poison deals 3 damage; its timer is now 4.
    # Player casts Magic Missile, dealing 4 damage.
    boss_turn = boss_turn ^ True
    effects = turn(player, boss, boss_turn, effects, lambda: magic_missile(player, boss))

    # -- Boss turn --
    # - Player has 2 hit points, 0 armor, 24 mana
    # - Boss has 3 hit points
    # Poison deals 3 damage. This kills the boss, and the player wins
    boss_turn = boss_turn ^ True
    effects = turn(player, boss, boss_turn, effects, lambda: _)

    print("Total mana", player.mana_spent)

    # --------------------------------------------------------------------------
    # Now, suppose the same initial conditions, except that the boss has 14 hit points instead:
    player = Character('Player', 10, 250, 0, 0)
    boss = Character('Boss', 14, 0, 8, 0)
    effects = []

    # -- Player turn --
    # - Player has 10 hit points, 0 armor, 250 mana
    # - Boss has 14 hit points
    # Player casts Recharge.
    boss_turn = False
    effects = turn(player, boss, boss_turn, effects, lambda: recharge(player))

    # -- Boss turn --
    # - Player has 10 hit points, 0 armor, 21 mana
    # - Boss has 14 hit points
    # Recharge provides 101 mana; its timer is now 4.
    # Boss attacks for 8 damage!    boss_turn = boss_turn ^ True

    boss_turn = boss_turn ^ True
    effects = turn(player, boss, boss_turn, effects, lambda: _)

    # -- Player turn --
    # - Player has 2 hit points, 0 armor, 122 mana
    # - Boss has 14 hit points
    # Recharge provides 101 mana; its timer is now 3.
    # Player casts Shield, increasing armor by 7.
    boss_turn = boss_turn ^ True
    effects = turn(player, boss, boss_turn, effects, lambda: shield(player))

    # -- Boss turn --
    # - Player has 2 hit points, 7 armor, 110 mana
    # - Boss has 14 hit points
    # Shield's timer is now 5.
    # Recharge provides 101 mana; its timer is now 2.
    # Boss attacks for 8 - 7 = 1 damage!
    boss_turn = boss_turn ^ True
    effects = turn(player, boss, boss_turn, effects, lambda: _)

    # -- Player turn --
    # - Player has 1 hit point, 7 armor, 211 mana
    # - Boss has 14 hit points
    # Shield's timer is now 4.
    # Recharge provides 101 mana; its timer is now 1.
    # Player casts Drain, dealing 2 damage, and healing 2 hit points.
    boss_turn = boss_turn ^ True
    effects = turn(player, boss, boss_turn, effects, lambda: drain(player, boss))

    # -- Boss turn --
    # - Player has 3 hit points, 7 armor, 239 mana
    # - Boss has 12 hit points
    # Shield's timer is now 3.
    # Recharge provides 101 mana; its timer is now 0.
    # Recharge wears off.
    # Boss attacks for 8 - 7 = 1 damage!
    boss_turn = boss_turn ^ True
    effects = turn(player, boss, boss_turn, effects, lambda: _)

    # -- Player turn --
    # - Player has 2 hit points, 7 armor, 340 mana
    # - Boss has 12 hit points
    # Shield's timer is now 2.
    # Player casts Poison.
    boss_turn = boss_turn ^ True
    effects = turn(player, boss, boss_turn, effects, lambda: poison(player, boss))

    # -- Boss turn --
    # - Player has 2 hit points, 7 armor, 167 mana
    # - Boss has 12 hit points
    # Shield's timer is now 1.
    # Poison deals 3 damage; its timer is now 5.
    # Boss attacks for 8 - 7 = 1 damage!
    boss_turn = boss_turn ^ True
    effects = turn(player, boss, boss_turn, effects, lambda: _)

    # -- Player turn --
    # - Player has 1 hit point, 7 armor, 167 mana
    # - Boss has 9 hit points
    # Shield's timer is now 0.
    # Shield wears off, decreasing armor by 7.
    # Poison deals 3 damage; its timer is now 4.
    # Player casts Magic Missile, dealing 4 damage.
    boss_turn = boss_turn ^ True
    effects = turn(player, boss, boss_turn, effects, lambda: magic_missile(player, boss))

    # -- Boss turn --
    # - Player has 1 hit point, 0 armor, 114 mana
    # - Boss has 2 hit points
    # Poison deals 3 damage. This kills the boss, and the player wins.
    boss_turn = boss_turn ^ True
    effects = turn(player, boss, boss_turn, effects, lambda: _)

    print("Total mana", player.mana_spent)


def play_part1():
    # You start with 50 hit points and 500 mana points.
    # Hit Points: 51
    # Damage: 9
    # What is the least amount of mana you can spend and still win the fight?
    # (Do not include mana recharge effects as "spending" negative mana.)
    player = Character('Player', 50, 500, 0, 0)
    boss = Character('Boss', 51, 0, 9, 0)
    effects = []

    # shield = 113 mana for 6*7 hp 42hp
    # 3x poison = 18 x 3 = 53 dmg for 519 mana (18 turns)
    # 2x poison = 36 dmg for 364 mana + 4x missile = 16 dmg for 212 mana = 576 total mana (16 turns)
    # recharge 505 - 229 = 276 mana over 5 turns
    # 50 / 9 = we get 12 turns
    # 92 / 9 = we get 22 turns => *need 1 shield*
    # 113 + 576 = 689 mana to kill as cheaply as possible => *need 1 recharge*
    # but we also need filler spells since we need to cast a spell every turn

    effects = turn(player, boss, False, effects, lambda: poison(player, boss))
    effects = turn(player, boss, True, effects, lambda: _)

    effects = turn(player, boss, False, effects, lambda: recharge(player))
    effects = turn(player, boss, True, effects, lambda: _)

    effects = turn(player, boss, False, effects, lambda: shield(player))
    effects = turn(player, boss, True, effects, lambda: _)

    effects = turn(player, boss, False, effects, lambda: poison(player, boss))
    effects = turn(player, boss, True, effects, lambda: _)

    effects = turn(player, boss, False, effects, lambda: magic_missile(player, boss))
    effects = turn(player, boss, True, effects, lambda: _)

    effects = turn(player, boss, False, effects, lambda: magic_missile(player, boss))
    effects = turn(player, boss, True, effects, lambda: _)

    effects = turn(player, boss, False, effects, lambda: magic_missile(player, boss))
    effects = turn(player, boss, True, effects, lambda: _)

    effects = turn(player, boss, False, effects, lambda: magic_missile(player, boss))
    print("Total mana", player.mana_spent)


def bump(combo, spells, pos):
    if abs(pos) == len(combo) + 1:
        return

    if combo[pos] == spells[-1]:
        combo[pos] = spells[0]
        bump(combo, spells, pos - 1)
    else:
        combo[pos] = spells[spells.index(combo[pos]) + 1]


INVALID_PATTERNS = set(['rrr', 'sss', 'ppp', 'rr', 'ss', 'pp'])
def is_valid_spell_pattern(combo):
    for i in range(0, len(combo)-1):
        if combo[i]+combo[i+1] in INVALID_PATTERNS:
            return False
        if i < len(combo) - 2:
            if combo[i]+combo[i+1]+combo[i+2] in INVALID_PATTERNS or \
            combo[i]+combo[i+2] in INVALID_PATTERNS:
                return False

    return True


def combos(spells, length):
    combo = [spells[0]]*length
    amount = pow(len(spells), length)
    print("Generating and validating", amount, "combinations...", end='')

    for i in range(amount):
        if is_valid_spell_pattern(combo):
            yield combo
        bump(combo, spells, -1)

        if i % (amount / 1000) == 0:
            print('.', end='', flush=True)


def play_part2_brute():
    # At the start of each player turn (before any other effects apply), you lose 1 hit point.
    spells = ['d', 'm', 'p', 'r', 's']

    min_mana = float('inf')
    min_combo = None
    for combo in combos(spells, 8):
        player = Character('Player', 50, 500, 0, 0)
        boss = Character('Boss', 51, 0, 9, 0)
        effects = []

        for spell in combo:
            if spell == 'p':
                l = lambda: poison(player, boss)
            elif spell == 'r':
                l = lambda: recharge(player)
            elif spell == 's':
                l = lambda: shield(player)
            elif spell == 'm':
                l = lambda: magic_missile(player, boss)
            elif spell == 'd':
                l = lambda: drain(player, boss)

            try:
                effects = turn(player, boss, False, effects, l, hard_mode=True)

                if effects is None and player.alive() and not boss.alive():
                    if player.mana_spent < min_mana:
                        min_mana = player.mana_spent
                        min_combo = copy.deepcopy(combo)
                    continue

                effects = turn(player, boss, True, effects, lambda: _, hard_mode=True)

                if effects is None and player.alive() and not boss.alive():
                    if player.mana_spent < min_mana:
                        min_mana = player.mana_spent
                        min_combo = copy.deepcopy(combo)
                    continue
            except Exception:
                continue

    print()
    print(min_mana, min_combo)


def main():
    test()

    # solved by trial and error
    play_part1()

    # try em all
    global LOGLEVEL
    LOGLEVEL = 'info'
    play_part2_brute()

if __name__ == '__main__':
    sys.exit(main())
