import collections
import time
import re
import sys
from itertools import cycle

day_str = "07"
test_input = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

test_input_2 = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""


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


def make_tuples(inputs):
    inputs = [x.replace(' bags', '').replace(' bag', '').replace('.', '') for x in inputs]

    # tuple of (outer, count, contained)
    all_tuples = []
    for x in inputs:
        outer = x.split(' contain ')[0]
        inner = x.split(' contain ')[1].split(', ')
        for dest in inner:
            if dest == 'no other':
                pass
            else:
                all_tuples.append((outer, dest.split(' ')[0], ' '.join(dest.split(' ')[1:])))

    return all_tuples


def find_all_containing(all_tuples, color):
    containing_colors = []

    for x in all_tuples:
        if x[2] == color:
            containing_colors.append(x[0])

    # dedupe
    containing_colors = list(set(containing_colors))

    recursive_result = []
    for this_color in containing_colors:
        recursive_result += find_all_containing(all_tuples, this_color)

    containing_colors = containing_colors + recursive_result
    containing_colors = list(set(containing_colors))
    return containing_colors


def solve_part1(start):
    inputs = load_inputs()
    all_tuples = make_tuples(inputs)

    # trace backwards from shiny gold
    return len(find_all_containing(all_tuples, 'shiny gold'))


def find_all_contained(all_tuples, color):
    contained = []

    for x in all_tuples:
        if x[0] == color:
            int_val = int(x[1])
            contained += [x[2]] * int_val

    recursive_result = []
    for x in contained:
        recursive_result += find_all_contained(all_tuples, x)

    return contained + recursive_result


def solve_part2(start):
    inputs = load_inputs()
    all_tuples = make_tuples(inputs)

    # trace forwards from shiny gold
    return len(find_all_contained(all_tuples, 'shiny gold'))


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
