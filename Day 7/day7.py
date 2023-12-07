import collections

file = open("input.txt")
lines = file.read().splitlines()
file.close()

rounds = (line.split(' ') for line in lines)
rounds = ((r[0], int(r[1])) for r in rounds)

types_text = {
    0: "High Card",
    1: "One Pair",
    2: "Two Pair",
    3: "Three of a Kind",
    4: "Full House",
    5: "Four of a Kind",
    6: "Five of a Kind"
}

card_power = []

def get_type_from_matchings(matching_counts):
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
    matching_counts = collections.Counter(hand_counts.values())
    return get_type_from_matchings(matching_counts)

def types_comparison(types):
    type, hand, _ = types
    card_power = {
        'T': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14
    }
    return (type,)+tuple(card_power[c] if c in card_power else int(c) for c in hand)


# Calculate the type for each hand
types = [(get_type_from_hand(hand),)+(hand, bid) for (hand, bid) in rounds]
types.sort(key=types_comparison)

# Get the winnings from these hands
winnings = [(i+1) * bid for i, (*_, bid) in enumerate(types)]
print(sum(winnings))
