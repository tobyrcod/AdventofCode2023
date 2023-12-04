import numpy as np

file = open("input.txt")
lines = file.read().splitlines()
file.close()

lines = [line[line.find(':') + 2:] for line in lines]
cards = [[set(map(int, p.split())) for p in line.split(' | ')] for line in lines]

def part1():
    points = 0
    for winner, given in cards:
        matched = given.intersection(winner)
        if matched:
            score = pow(2, len(matched) - 1)
            points += score

    print(points)

def part2():
    # Convert each card into a set of card ids it wins you
    card_prizes = dict()
    for i, (winner, given) in enumerate(cards):
        matched = given.intersection(winner)
        card_prizes[i] = np.arange(1, len(matched) + 1, dtype=int) + i

    # Now we know the prizes for each card, we can play the game
    hand = np.ones(len(cards), dtype=int)
    for i, quantity in enumerate(hand):
        for prize in card_prizes[i]:
            hand[prize] += quantity

    print(sum(hand))


part2()
