#!/usr/bin/env python3

import sys
from functools import reduce


def create_combinations():
    for a in range(1, 98):
        for b in range(1, 98):
            if a+b > 100:
                break

            for c in range(1, 98):
                if a+b+c > 100:
                    break

                for d in range(1, 98):
                    if a+b+c+d > 100:
                        break

                    if a+b+c+d == 100:
                        yield a, b, c, d


def prod(l):
    return reduce((lambda x, y: x * y), l)


def main():
    # Sugar: capacity 3, durability 0, flavor 0, texture -3, calories 2
    # Sprinkles: capacity -3, durability 3, flavor 0, texture 0, calories 9
    # Candy: capacity -1, durability 0, flavor 4, texture 0, calories 1
    # Chocolate: capacity 0, durability 0, flavor -2, texture 2, calories 8
    ingredients = [
        (3, 0, 0, -3, 2),
        (-3, 3, 0, 0, 9),
        (-1 ,0, 4, 0, 1),
        (0, 0, -2, 2, 8)
    ]

    max_product = 0
    max_combo = None
    max_product_calories = 0
    max_combo_calories = None
    for c in create_combinations():
        parts = []
        for i in range(4):
            parts.append(c[0] * ingredients[0][i] + c[1] * ingredients[1][i] + c[2] * ingredients[2][i] + c[3] * ingredients[3][i])

            if parts[i] < 0:
                parts[i] = 0

        calories = c[0] * ingredients[0][4] + c[1] * ingredients[1][4] + c[2] * ingredients[2][4] + c[3] * ingredients[3][4]
        product = prod(parts)
        if calories == 500:
            if product > max_product_calories:
                max_product_calories = product
                max_combo_calories = c

        if product > max_product:
            max_product = product
            max_combo = c

    print(max_combo, max_product)
    print(max_combo_calories, max_product_calories)


if __name__ == '__main__':
    sys.exit(main())
