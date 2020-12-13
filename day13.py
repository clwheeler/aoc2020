import collections
import time
import re
import sys
from itertools import cycle

day_str = "13"
test_input = """939
7,13,x,x,59,x,31,19"""

test_input_2 = """939
17,x,13,19"""

test_input_3="""939
67,7,59,61
"""

test_input_3="""939
1789,37,47,1889
"""



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


def solve_part1(start):
    inputs = load_inputs()
    start_time = int(inputs[0])
    buses = [int(x) for x in inputs[1].split(',') if x != 'x']
    mods = [x - (start_time % x) for x in buses]
    min_index = mods.index(min(mods))
    return mods[min_index] * buses[min_index]


# returns n where n % val_a == 0 and (n + index_diff) % val_b == 0
# this means that val_a stops on the minute, and val_b stops index_diff
# minutes later
def get_intersection_data(start, val_a, val_b, index_diff):
    start_val = start
    values_found = []

    while len(values_found) <= 2:
        if (start_val + index_diff) % val_b == 0:
            values_found.append(start_val)
            print start_val, '<='
        else:
            pass
            print start_val
        start_val += val_a

    first_intersection = values_found[0]
    repeat_period = values_found[1] - values_found[0]
    return first_intersection, repeat_period


def solve_part2(start):
    test = """1
67,7,59,61"""
    inputs = load_inputs(test)
    buses = [int(x) for x in inputs[1].split(',') if x != 'x']
    bus_indexes = [x for x in inputs[1].split(',')]

    # there is some periodicity to the alignment between 1 and 2,
    # and futher periodicity to the alignment between [1, 2] and 3
    # etc.
    #
    # For 3, 5, 4:
    # 3, 5 repeats every 5 elems from X: (3, 8, 13, 18, 23, 28, 33..)
    # (3, 5), 4 first happens at (X), then repeats every Y elems (5 * 4?)
    #
    print buses
    print bus_indexes

    start_val = 0
    previous_value = 0

    for ind, orig_bus_id in enumerate(buses):
        if ind == len(buses) - 1:
            # break on last element
            break

        bus_id = previous_value
        if not bus_id:
            bus_id = orig_bus_id

        next_bus = buses[ind + 1]

        bus_index = bus_indexes.index(str(orig_bus_id))
        next_bus_index = bus_indexes.index(str(next_bus))
        index_diff = next_bus_index - bus_index
        print bus_id, next_bus, index_diff, 'start from', start_val
        first_intersection, repeat_period = get_intersection_data(start_val, bus_id, next_bus, index_diff)

        # on the next iteration, we use repeat_period as though it was the previous bus_id
        start_val = first_intersection
        previous_value = repeat_period

        print bus_id, next_bus, 'intersect at {}, repeats after {}'.format(first_intersection, repeat_period)
        # starting at the first_intersection, step by repeat_period

    # return "TODO"


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
