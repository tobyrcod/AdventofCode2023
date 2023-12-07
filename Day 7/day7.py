import collections

file = open("input.txt")
lines = file.read().splitlines()
file.close()

# part1: False, part2: True
ALLOW_JOKERS = True

rounds = (line.split(' ') for line in lines)
rounds = ((r[0], int(r[1])) for r in rounds)

def get_type_from_matching_counts(matching_counts, joker_count=0):
    def get_lowest_number_of_jokers_needed(target, jokers, mc=matching_counts):
        # If we can use i jokers to reach the target t matching, return i
        # If no amount of jokers will get us there, return -1
        return next((i for i in range(0, jokers+1) if target-i in mc), -1)

    # Can we trivially make 5 of a kind?
    if joker_count >= 4:
        return 6

    # Can we make 5 by using n jokers?
    n = get_lowest_number_of_jokers_needed(target=5, jokers=joker_count)
    if n != -1:
        # Five of a kind
        return 6

    # Can we make 4 by using n jokers?
    n = get_lowest_number_of_jokers_needed(target=4, jokers=joker_count)
    if n != -1:
        # Four of a kind
        return 5

    # Can we make 3 by using n jokers?
    n = get_lowest_number_of_jokers_needed(target=3, jokers=joker_count)
    if n != -1:
        """
        We have a 3 of a kind
        We can't have any jokers remaining
        (if we did, we could trivially make a 4 of a kind)
        """
        new_matching_counts = {key: val for (key, val) in matching_counts.items()}
        new_matching_counts[3-n] -= 1
        if new_matching_counts[3-n] == 0:
            del new_matching_counts[3-n]
        if 2 in new_matching_counts:
            return 4
        return 3
    """
    At this stage, we know joker count is 0 or 1 
    (if joker count was >= 2, we could trivially make a 3 of a kind)
    
    If we have a joker, we must have junk
    (If we had a pair, then trivially with the joker we could make 3 of a kind)
    
    You cant have junk with a joker
    (you can trivially make 1 pair)
    """
    if joker_count > 0:
        # One Pair
        return 1

    # No jokers, so proceed as normal
    if len(matching_counts) == 1:
        # Junk / High Card
        return 0

    if matching_counts[2] > matching_counts[1]:
        # Two pair
        return 2
    # One Pair
    return 1

def get_type_from_hand(hand):
    hand_counts = collections.Counter(hand)
    joker_count = 0
    if ALLOW_JOKERS and 'J' in hand_counts:
        # If we allow jokers, and we have some jokers
        joker_count = hand_counts['J']
        del hand_counts['J']

    matching_counts = collections.Counter(hand_counts.values())
    return get_type_from_matching_counts(matching_counts, joker_count)

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
