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

test_input_4="""939
3,5,7
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


# returns first n where n % val_a == 0 and (n + index_diff) % val_b == 0
# this means that val_a stops on the minute, and val_b stops index_diff
# minutes later
def get_intersection_data(start, val_a, val_b, index_diff):
    start_val = start
    values_found = []

    # print 'Calculating {}, {}, {}, {}'.format(start_val, val_a, val_b, index_diff, val_b)

    while len(values_found) <= 2:
        # print 'Calculating {}+ {} % {} == {}'.format(start_val, index_diff, val_b, (start_val + index_diff) % val_b)
        if (start_val + index_diff) % val_b == 0:
            values_found.append(start_val)
            # print start_val, '<='
        else:
            pass
            # print start_val
        start_val += val_a

    first_intersection = values_found[0]
    repeat_period = values_found[1] - values_found[0]
    return first_intersection, repeat_period


def solve_part2_naive(start):
    inputs = load_inputs(test_input_3)
    buses = [int(x) for x in inputs[1].split(',') if x != 'x']
    bus_indexes = [x for x in inputs[1].split(',')]

    max_val = max(buses)
    max_index = bus_indexes.index(str(max_val))
    print "largest value {} at t+{}".format(max_val, max_index)
    print "t=0 must be {} plus a multiple of {}".format(max_val-max_index, max_val)

    start_val = max_val - max_index
    stop_loop = False

    while not stop_loop:
        print start_val
        start_val += max_val
        for bus in buses:
            bus_index = bus_indexes.index(str(bus))
            if (start_val + bus_index) % bus != 0:
                stop_loop = False
                break
            else:
                stop_loop = True

    print start_val
    return "TODO"



def solve_part2(start):
    inputs = load_inputs()
    buses = [int(x) for x in inputs[1].split(',') if x != 'x']
    bus_indexes = [x for x in inputs[1].split(',')]

    # There is some periodicity to the alignment between b1 and b2,
    # and futher periodicity to the alignment between [b1 + b2] and b3
    # etc.
    #
    # For [3,5,7]:
    # 3, 5 repeats every 15 steps, starting from 9:
    #   3*3 = 9 = 10-1
    #   3*8 = 24 = 25-1
    #   3*13 = 39 = 40-1
    # This is equivalent to a single bus with period 15 (beginning at 9):
    #   9, 24, 39, 54...
    # We can then computer the intersections between this multi-bus pack and
    # the next bus in the chain. We subtract 2 because the multi bus is
    # equivalent to a single bus going at time 0.
    #   9+(15*3) = 54 = 56-2
    #   9+(15*10) = 159 = 161-2
    #   9+(15*17) = 264 = 266-2

    start_val = 0
    previous_value = 0
    first_intersections = []

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
        index_diff = next_bus_index
        # print bus_id, next_bus, '+{}'.format(index_diff), 'start from', start_val
        first_intersection, repeat_period = get_intersection_data(start_val, bus_id, next_bus, index_diff)
        first_intersections.append(first_intersection)
        # on the next iteration, we use repeat_period as though it was the previous bus_id
        start_val = first_intersection
        previous_value = repeat_period

        # print bus_id, next_bus, 'intersect at {}, repeats after {}'.format(first_intersection, repeat_period)
        # starting at the first_intersection, step by repeat_period

    return first_intersections[-1]
    # return "TODO"


def run():

    start_time = time.time()
    print "Part 1:"
    print solve_part1(0)
    print "Runtime: {} seconds".format(time.time() - start_time)

    start_time = time.time()
    print "Part 2:"
    # print solve_part2_naive(0)
    print solve_part2(0)
    print "Runtime: {} seconds".format(time.time() - start_time)

run()
