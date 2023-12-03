file = open("input1.txt")
lines = file.read().splitlines()
file.close()


def part1():
    codes = []
    for line in lines:
        # pointers
        left = 0
        right = len(line) - 1

        # digits
        first = last = None
        while not (first and last):  # Assuming first and last digits always present
            lc = line[left]
            rc = line[right]

            if not first and lc.isdigit():
                first = lc

            if not last and rc.isdigit():
                last = rc

            left += 1
            right -= 1

        codes.append(int(first + last))

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

    codes = []
    for line in lines:
        code = ''

        for word, edges, f in [(line, forward_edges, None), (line[::-1], backward_edges, lambda s: s[::-1])]:
            paths = []
            i = 0
            found = False
            while not found and i < len(word):
                newchar = word[i]
                if newchar.isdigit():
                    code += newchar
                    found = True
                    break

                #
                # We can either add the new char to the end of the current path
                # Or make a new path starting with the new char
                # Then whichever reaches a valid digit first wins

                remove_paths = []
                for j in range(len(paths)):
                    valid_moves = edges[paths[j]]
                    if newchar in valid_moves:
                        paths[j] += newchar
                    else:
                        remove_paths.append(paths[j])

                    if paths[j] not in edges:
                        digit_word = paths[j] if not f else f(paths[j])
                        digit_char = str(digit_words.inverse[digit_word])
                        code += digit_char
                        found = True
                        break

                if newchar in edges.keys():
                    paths.append(newchar)

                for path in remove_paths:
                    paths.remove(path)

                i += 1

        codes.append(int(code))
    print(sum(codes))


part2()
