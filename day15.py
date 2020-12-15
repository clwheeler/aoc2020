from collections import defaultdict
import time
import re
import sys
from itertools import cycle

day_str = "00"

test_input = """x"""
input_list = [0, 3, 1, 6, 7, 5]


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
    parsed = inputs.split('\n')
    return parsed


def findall(target, find_in):
    """ Returns all matching indexes
    """
    matching_indexes = []
    for ind, x in enumerate(find_in):
        if x == target:
            matching_indexes.append(ind)

    return matching_indexes


def solve_part1(steps):
    """ There are lots of more efficient ways to do this, but complexity 2020
        isn't really an issue. I assume part 2 will be like 2020 million
    """
    inputs = input_list
    full_list = [x for x in inputs]

    for x in xrange(steps-len(inputs)):
        last_num = full_list[-1]
        matches = findall(last_num, full_list[:-1])
        if len(matches) == 0:
            next_num = 0
        else:
            next_num = (len(full_list)-1) - matches[-1]

        full_list.append(next_num)

    return full_list[-1]


def solve_part2(steps):
    """ This is something like n*logn (n dict lookups) for n steps as opposed
        to n^2 (n^n?) for the part 1 solution (scan the entire history list n times).
    """
    inputs = input_list
    # store when a number was last seen
    last_indexes = defaultdict(int)
    last_num = 0

    for x in xrange(steps):
        this_num = 0
        if x < len(inputs):
            this_num = inputs[x]
        else:
            # lookup previous value
            last_index = last_indexes[last_num]

            if last_index == 0:
                this_num = 0
            else:
                this_num = x - last_index

        # don't add the previous value until we're done with our lookups
        last_indexes[last_num] = x
        last_num = this_num

    return last_num


def run():

    start_time = time.time()
    print "Part 1:"
    print solve_part1(2020)
    print "Runtime: {} seconds".format(time.time() - start_time)

    start_time = time.time()
    print "Part 2:"
    print solve_part2(30000000)
    print "Runtime: {} seconds".format(time.time() - start_time)

run()
