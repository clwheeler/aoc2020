import collections
import time
import re
import sys
from itertools import cycle

day_str = "06"
test_input = """abc

a
b
c

ab
ac

a
a
a
a

b"""


def load_inputs(input_str=None):
    inputs = []

    if input_str:
        inputs = input_str
    else:
        with open('./inputs/day{}_input.txt'.format(day_str), 'r') as f:
            inputs = f.read()

    parsed_test_input = parse_inputs(inputs)
    return parsed_test_input


def parse_inputs(inputs):
    parsed = inputs.split('\n\n')
    parsed = [x.replace('\n', ' ') for x in parsed]
    return parsed


def solve_part1(start):
    inputs = load_inputs()
    deduped = [list(set(x.replace(' ', ''))) for x in inputs]
    all_lens = [len(x) for x in deduped]
    return sum(all_lens)

def char_range(c1, c2):
    """Generates the characters from `c1` to `c2`, inclusive."""
    for c in xrange(ord(c1), ord(c2)+1):
        yield chr(c)

def solve_part2(start):
    inputs = load_inputs()
    print inputs
    all_lists = []
    for x in inputs:
        entries = x.count(' ') + 1
        all_contain_list = []
        for char in char_range('a', 'z'):
            if x.count(char) == entries:
                all_contain_list.append(char)
        all_lists.append(all_contain_list)

    all_lens = [len(x) for x in all_lists]
    return sum(all_lens)


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
