import collections
import time
import re
import sys
from itertools import cycle


def load_inputs(day_str):
    inputs = []
    # parse input data
    with open('./inputs/day{}_input.txt'.format(day_str), 'r') as f:
        for line in f:
            inputs.append(line.rstrip())
    return inputs

def load_test():
    pass


def solve_part1(start):
    inputs = load_inputs('01')
    inputs = [int(x) for x in inputs]
    for x_ct, x in enumerate(inputs):
        for y_ct, y in enumerate(inputs):
            print x, y, x + y
            if x_ct != y_ct:
                if x+y == 2020:
                    return (x, y, x * y)


def solve_part2(start):
    inputs = load_inputs('01')
    inputs = [int(x) for x in inputs]
    for x_ct, x in enumerate(inputs):
        for y_ct, y in enumerate(inputs):
            for z_ct, z in enumerate(inputs):
                if x_ct != y_ct and x_ct != z_ct:
                    if x+y+z == 2020:
                        return (x, y, z, x * y * z)




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
