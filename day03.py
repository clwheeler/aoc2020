import collections
import time
import re
import sys
from itertools import cycle

DEBUG = False
day_str = "03"
test_input = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""


def load_inputs():
    inputs = []
    with open('./inputs/day{}_input.txt'.format(day_str), 'r') as f:
        for line in f:
            inputs.append(line.rstrip())
    inputs = parse_inputs(inputs)
    return inputs


def load_test_inputs():
    parsed_test_input = test_input.splitlines()
    parsed_test_input = parse_inputs(parsed_test_input)
    return parsed_test_input


def parse_inputs(inputs):
    parsed = [x for x in inputs]
    return parsed


def solveForSlope(dx, dy):
    """
    Since we know that the pattern simply repeats, we can use cycle to avoid having
    to keep the entire grid in memory. We could do also do some modulo arithmetic on the
    indexes to achieve an equivalent effect.

    It feels sloppy to catch the StopIteration error, but EAFP
    """
    inputstr = load_inputs()

    treecount = 0
    x_index = 0

    y_iter = iter(xrange(len(inputstr)))

    for y_index in y_iter:
        cycler = cycle(inputstr[y_index])
        elem = ''

        if DEBUG:
            elemlist = []
            for x in xrange(x_index + 1):
                elemlist.append(cycler.next())
            print elemlist
        else:
            for x in xrange(x_index + 1):
                elem = cycler.next()
            if elem == '#':
                treecount += 1

        x_index += dx
        for y_inc in range(dy-1):
            try:
                y_iter.next()
            except StopIteration:
                pass

    return treecount


def solve_part1(start):
    return solveForSlope(3, 1)


def solve_part2(start):
    return solveForSlope(1, 1) * solveForSlope(3, 1) * solveForSlope(5, 1) * solveForSlope(7, 1) * solveForSlope(1, 2)


def run():

    start_time = time.time()
    print "Part 1:"
    print solve_part1(0)
    print "Runtime: {} seconds".format(time.time() - start_time)

    start_time = time.time()
    print "Part 2:"
    print solve_part2(0)
    print "Runtime: {} seconds".format(time.time() - start_time)

run()
