import collections
import time
import re
import sys
from itertools import cycle

day_str = "17"
test_input = """.#.
..#
###"""


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


def get_all_neighbors(pos, fourth_dim=False):
    """
    Get all neighbors around a point (inclusive)
    """
    bounds = (-1, 0, 1)
    neighbors = []
    for x in bounds:
        for y in bounds:
            for z in bounds:
                if fourth_dim:
                    for w in bounds:
                        neighbors.append((pos[0]+x, pos[1]+y, pos[2]+z, pos[3]+w))
                else:
                    neighbors.append((pos[0]+x, pos[1]+y, pos[2]+z))

    return neighbors


def get_active_neighbors(p_set, pos, fourth_dim=False):
    """
    Get active neighbors around a point (exclusive)
    """
    neighbors = get_all_neighbors(pos, fourth_dim)
    neighbors.remove(pos)
    active = [n for n in neighbors if n in p_set]

    return active


def solve_part1(start):
    """
    We only really care about elements with status=Active, and we only care
    about direct lookups, so let's just keep them in a set
    """
    inputs = load_inputs()
    # initialize onto the x, y plane where z=0
    active_set = set()
    for y, row in enumerate(inputs):
        for x, col in enumerate(row):
            if col == '#':
                active_set.add((x, y, 0))

    # active_set = set([(0, 0, 0), (2, 0, 0)])
    # print "active", active_set
    steps = 6
    for rnd in xrange(steps):
        next_active_set = set()
        # the only ones that can become active have at least one active neighbor
        # so lets just make a list of all neighbors for each elem
        candidates = []
        for point in active_set:
            candidates += get_all_neighbors(point)

        print "considering {} candidates...".format(len(candidates))

        for pos in candidates:
            neighbors = get_active_neighbors(active_set, pos)
            if pos in active_set:
                if len(neighbors) in [2, 3]:
                    next_active_set.add(pos)
            elif len(neighbors) == 3:
                next_active_set.add(pos)

        active_set = next_active_set.copy()

    return len(active_set)


def solve_part2(start):
    """
    We only really care about elements with status=Active, and we only care
    about direct lookups, so let's just keep them in a set
    """
    inputs = load_inputs()
    # initialize onto the x, y plane where z=0
    active_set = set()
    for y, row in enumerate(inputs):
        for x, col in enumerate(row):
            if col == '#':
                active_set.add((x, y, 0, 0))

    # active_set = set([(0, 0, 0), (2, 0, 0)])
    # print "active", active_set
    steps = 6
    for rnd in xrange(steps):
        next_active_set = set()
        # the only ones that can become active have at least one active neighbor
        # so lets just make a list of all neighbors for each elem
        candidates = []
        for point in active_set:
            candidates += get_all_neighbors(point, True)

        print "considering {} candidates...".format(len(candidates))

        for pos in candidates:
            neighbors = get_active_neighbors(active_set, pos, True)
            if pos in active_set:
                if len(neighbors) in [2, 3]:
                    next_active_set.add(pos)
            elif len(neighbors) == 3:
                next_active_set.add(pos)

        active_set = next_active_set.copy()

    return len(active_set)


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
