import sys

import numpy as np
import sympy

"""
Noticed all sequences are polynomial =>
Maybe generating functions / discrete math =>
sympy / lagrange polynomials:
From Wikipedia (https://en.wikipedia.org/wiki/Lagrange_polynomial#Definition)
In numerical analysis, the Lagrange interpolating polynomial 
is the unique polynomial of lowest degree that 
interpolates a given set of data

From Wolfram MathWorld, 
Lagrange Interpreting Polynomial:
(https://mathworld.wolfram.com/LagrangeInterpolatingPolynomial.html)
Also, think the AOC instructions describe Neville's Algorithm:
(https://mathworld.wolfram.com/NevillesAlgorithm.html)
"""

file = open("test1.txt")
lines = file.read().splitlines()
file.close()

sequences = [list(map(int, line.split())) for line in lines]
num_sequences = len(sequences)

# part1: FIND_NEXT_TERM = True
# part2: FIND_PREVIOUS_TERM = True
FIND_NEXT_TERM = True
FIND_PREVIOUS_TERM = True

def lagrangepoly(yseq):
    # Algo from Wolfram MathWorld (above)
    x = sympy.symbols('x')

    result = 0
    for j, yj in enumerate(yseq):
        prod = 1
        for k, yk in enumerate(yseq):
            if k == j:
                continue
            prod *= (x - (k + 1)) / (j - k)
        result += yj * prod
    return sympy.expand(result)

nexts = list()
previouses = list()
print('Progress:')
for i, sequence in enumerate(sequences):
    print(i / num_sequences)
    nth_term = lagrangepoly(sequence)

    nexts.append(nth_term.subs('x', len(sequence) + 1))
    previouses.append(nth_term.subs('x', 0))
print('--------')

if FIND_NEXT_TERM:
    print(sum(nexts), nexts)
if FIND_PREVIOUS_TERM:
    print(sum(previouses), previouses)
