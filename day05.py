import collections
import time
import re
import sys
from itertools import cycle

day_str = "05"
test_input = """FBFBBFFRLR
BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL"""
# BFFFBBFRRR: row 70, column 7, seat ID 567.
# FFFBBBFRRR: row 14, column 7, seat ID 119.
# BBFFBBFRLL: row 102, column 4, seat ID 820.

def load_inputs(input_str=None):
    inputs = []

    if input_str:
        inputs = input_str.splitlines()
    else:
        with open('./inputs/day{}_input.txt'.format(day_str), 'r') as f:
            for line in f:
                inputs.append(line.rstrip())

    parsed_test_input = parse_inputs(inputs)
    return parsed_test_input


def parse_inputs(inputs):
    parsed = [x for x in inputs]
    return parsed


def get_all_seat_ids():
    inputs = load_inputs()
    seatids = []
    for seat in inputs:
        row = 0
        col = 0
        for ind, command in enumerate(seat):
            colind = ind - 6
            if command == 'F':
                row += 0
            elif command == 'B':
                row += int(128 / (2 ** (ind+1)))
            elif command == 'L':
                col += 0
            elif command == 'R':
                col += int(8 / (2 ** colind))
        seatid = row * 8 + col
        seatids.append(seatid)
    return seatids


def solve_part1(start):
    """
    This can probably be done with bit shift operators, but I don't know those in python :/
    """
    seatids = get_all_seat_ids()
    return max(seatids)


def solve_part2(start):
    seatids = get_all_seat_ids()
    seatids = sorted(seatids)
    for ind, x in enumerate(seatids):
        if ind == 0:
            continue
        if seatids[ind-1] != x - 1:
            return x-1

    return 0


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
