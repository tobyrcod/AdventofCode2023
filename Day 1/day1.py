file = open("input1.txt")
lines = file.read().splitlines()
file.close()


def part1():
    def find_digit(word, i, step):
        while 0 <= i < len(word):
            if line[i].isdigit():
                return i
            i += step

    codes = []
    for line in lines:
        # O(n), n is length of line
        left = find_digit(line, 0, 1)  # k steps s.t k < n
        right = find_digit(line, len(line)-1, -1)  # max of n-k steps

        codes.append(int(line[left] + line[right]))

    print(sum(codes))


def part2():
    # Ideas:
    # Just considering first digit for now
    # We look at the left pointer
    # If it is a digit, then we return
    # If it is a char, then we can search the substring upto now for a digit
    # Bonus: digit needs to end in the char at pointer, otherwise we would have found it last step
    from bidict import bidict

    #
    # Construct digit words (excluding zero as given)
    digit_words = bidict({
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine"
    })

    #
    # Almost predictive texty -
    # construct graph s,t, if I type 't' then valid following chars are
    # 'w' (two) and 'h' (three) etc

    forward_edges = dict()  # Adjacency list representation
    backward_edges = dict()  # Adjacency list representation
    for digit_word in digit_words.values():
        for word, edges in [(digit_word, forward_edges), (digit_word[::-1], backward_edges)]:
            prev_substring = None
            for i in range(len(word)):
                substring = word[:i + 1]

                if prev_substring:
                    if prev_substring not in edges:
                        edges[prev_substring] = set()
                    edges[prev_substring].add(substring[-1])

                prev_substring = substring

    #
    # Now when we see a char, we build up a memory
    # if we still have a valid path in the graph, we continue
    # if we run out of options, we start again with a new path

    def find_digit_in_word(word, edges, word_modifier):
        paths = []
        word = word_modifier(word)

        for char in word:
            if char.isdigit():
                return char

            #
            # We can either add the new char to the end of the current path
            # Or make a new path starting with the new char
            # Then whichever reaches a valid digit first wins

            remove_paths = []
            for i in range(len(paths)):
                valid_moves = edges[paths[i]]
                if char in valid_moves:
                    paths[i] += char
                else:
                    remove_paths.append(paths[i])

                # if the path grows enough to not have any more valid moves i.e complete digit
                if paths[i] not in edges:
                    digit_word = word_modifier(paths[i])
                    digit_char = str(digit_words.inverse[digit_word])
                    return digit_char

            for path in remove_paths:
                paths.remove(path)

            if char in edges.keys():
                paths.append(char)

    codes = []
    for line in lines:
        code = ''

        for word, edges, f in [(line, forward_edges, lambda s: s), (line, backward_edges, lambda s: s[::-1])]:
            digit = find_digit_in_word(word, edges, f)
            code += digit

        codes.append(int(code))
    print(sum(codes))

part1()
