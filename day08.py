import collections
import time
import re
import sys
from itertools import cycle

day_str = "08"
test_input = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

halting_input = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
nop -4
acc +6"""


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
    parsed = [x.split() for x in inputs.split('\n')]
    parsed = [(x[0], int(x[1])) for x in parsed]
    return parsed


# returns offset, accumulator
def execute_command(command_tuple, accum):
    offset = 0
    (command, value) = command_tuple
    if command == 'nop':
        offset = 1
    elif command == 'acc':
        offset = 1
        accum += value
    elif command == 'jmp':
        offset = value

    return offset, accum


def solve_for_commands(commands):
    visited_indexes = []
    command_pointer = 0
    accum = 0

    while True:
        if command_pointer in visited_indexes:
            break
        try:
            offset, accum = execute_command(commands[command_pointer], accum)
            visited_indexes.append(command_pointer)
            command_pointer += offset
        except IndexError:
            return "Halted", accum

    return "Loop Detected", accum


def solve_part1(inputs):
    commands = load_inputs()
    return solve_for_commands(commands)


def solve_part2(start):
    """
    Brute Force it.
    Search from the end, since halts would have to walk past the last instruction
    """
    baseline_commands = load_inputs()
    # build iterations
    for index in xrange(len(baseline_commands)):
        reverse_index = 0-(index+1)
        copy = [x for x in baseline_commands]
        this_command = copy[reverse_index]
        # mutate it if necessary
        if this_command[0] == 'jmp':
            copy[reverse_index] = ('nop', this_command[1])
            result = solve_for_commands(copy)
            if result[0] == 'Halted':
                return result


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
