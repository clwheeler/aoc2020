import collections
import time
import re
import sys
from itertools import cycle

day_str = "00"
test_input = """x"""


def load_inputs():
    inputs = []
    with open('./inputs/day{}_input.txt'.format(day_str), 'r') as f:
        for line in f:
            inputs.append(line.rstrip())
    inputs = parse_inputs(inputs)
    return inputs


def load_test_inputs(_):
    parsed_test_input = test_input.splitlines()
    parsed_test_input = parse_inputs(test_input)
    return parsed_test_input


def parse_inputs(inputs):
    parsed = [x.split(' ') for x in inputs]
    return parsed


def solve_part1(start):
    return "TODO"


def solve_part2(start):
    return "TODO"


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
