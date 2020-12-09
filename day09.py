from collections import deque
import time
import re
import sys
from itertools import permutations

day_str = "09"
test_input = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""


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
    parsed = [int(x) for x in parsed]
    return parsed


def solve_part1(window_len):
    inputs = load_inputs()
    window = deque(inputs[0:window_len])
    for target in inputs[window_len:]:
        sum_found = False
        for perm in permutations(window, 2):
            if sum(perm) == target:
                sum_found = True
                break
        if not sum_found:
            return target
        window.popleft()
        window.append(target)

    return "NOT FOUND"


def solve_part2(target):
    inputs = load_inputs()
    window = deque()
    for candidate in inputs:
        if sum(window) == target:
            return min(window) + max(window)
        if sum(window) < target:
            window.append(candidate)

        while sum(window) > target:
            window.popleft()

    return "NOT FOUND"


def run():

    start_time = time.time()
    print "Part 1:"
    print solve_part1(25)
    print "Runtime: {} seconds".format(time.time() - start_time)

    start_time = time.time()
    print "Part 2:"
    print solve_part2(solve_part1(25))
    print "Runtime: {} seconds".format(time.time() - start_time)

run()
