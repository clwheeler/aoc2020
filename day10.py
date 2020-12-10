from collections import defaultdict
import time
import re
import sys
from itertools import cycle

day_str = "10"
test_input = """16
10
15
5
1
11
7
19
6
12
4"""

test_input_2 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""

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
    parsed.sort()
    return parsed


def solve_part1(start):
    inputs = load_inputs()

    inputs = [0] + inputs + [inputs[-1] + 3]

    one_jolt_diffs = 0
    three_jolt_diffs = 0

    for ind, this_elem in enumerate(inputs):
        for comp_elem in inputs[ind:]:
            diff = comp_elem - this_elem
            if diff == 1:
                one_jolt_diffs += 1
                break
            elif diff == 3:
                three_jolt_diffs += 1
                break
            elif diff > 3:
                break

    return (one_jolt_diffs, three_jolt_diffs, one_jolt_diffs*three_jolt_diffs)


PATH_CACHE = dict()

def find_permutations(this_elem, adapter_list):
    """
    Use a cache to avoid re-computing the same paths repeatedly.

    """
    this_sum = 0

    if PATH_CACHE.get(this_elem, None):
        return PATH_CACHE[this_elem]

    if not adapter_list:
        PATH_CACHE[this_elem] = 1
        return 1

    for ind, adapter in enumerate(adapter_list):
        diff = adapter - this_elem
        if diff <= 3:
            this_sum += find_permutations(adapter, adapter_list[ind+1:])
        else:
            continue

    PATH_CACHE[this_elem] = this_sum
    return this_sum


def solve_part2(start):
    inputs = load_inputs()
    inputs = [0] + inputs + [inputs[-1] + 3]
    return find_permutations(inputs[0], inputs[1:])


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
