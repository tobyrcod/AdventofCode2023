import collections

file = open("input.txt")
lines = file.read().splitlines()
file.close()

# part1: False, part2: True
ALLOW_JOKERS = True

rounds = (line.split(' ') for line in lines)
rounds = ((r[0], int(r[1])) for r in rounds)

def get_type_from_matching_counts(matching_counts):
    if len(matching_counts) == 1:
        # Either Five of a kind or High card
        if 5 in matching_counts:
            # Five of a kind
            return 6
        # High card
        return 0
    if 4 in matching_counts:
        # Four of a kind
        return 5
    if 3 in matching_counts:
        # Either Full house or 3 of a kind
        if 2 in matching_counts:
            # Full house
            return 4
        # 3 of a kind
        return 3
    # Either Two Pair or One Pair
    if matching_counts[2] > matching_counts[1]:
        # Two pair
        return 2
    # One Pair
    return 1

def get_type_from_hand(hand):
    hand_counts = collections.Counter(hand)
    # If we allow jokers, and we have some jokers
    if ALLOW_JOKERS and 'J' in hand_counts:
        # Turn all the jokers into the card we already have the most of that isn't a joker
        # This trick only works because that strategy is always optimal for the hands we can make
        joker_count = hand_counts['J']
        del hand_counts['J']
        if hand_counts:
            hand_counts[max(hand_counts, key=hand_counts.get)] += joker_count
        else:
            # Edge case, if we had all jokers then we don't have a non-joker max
            # So we just make our own, as we would turn all jokers into the best card we can
            hand_counts['A'] = joker_count
    matching_counts = collections.Counter(hand_counts.values())
    return get_type_from_matching_counts(matching_counts)

def types_comparison(types):
    type, hand, _ = types
    card_power = {
        'T': 10,
        'J': 1 if ALLOW_JOKERS else 11,
        'Q': 12,
        'K': 13,
        'A': 14
    }
    return (type,)+tuple(card_power[c] if c in card_power else int(c) for c in hand)


# Calculate the type for each hand
round_values = [(get_type_from_hand(hand),)+(hand, bid) for (hand, bid) in rounds]
round_values.sort(key=types_comparison)

# Get the winnings from these hands
winnings = [(i+1) * bid for i, (*_, bid) in enumerate(round_values)]
print(sum(winnings))
