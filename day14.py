import collections
import time
import re
import sys
from itertools import cycle
from ctypes import c_uint64

day_str = "14"
test_input = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

test_input_2 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""

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
    parsed = [x.split(' = ') for x in parsed]
    return parsed


def solve_part1(start):
    inputs = load_inputs()
    # we use uint64 because we have > 32 bits
    # For Xs, retain original value (X & 1) = X, everything else = 0
    # turn Xs to 1s and digits to 0, and them
    # leave Xs alone, force other values to be the values from the mask
    # turn Xs to 0s, leave everything else alone, or them
    current_mask = ''
    registers = {}

    for command in inputs:
        if command[0] == 'mask':
            current_mask = command[1]
            # print "Setting mask to {}".format(command[1])
        else:
            and_mask = re.sub(r'0|1', '0', current_mask)
            and_mask = and_mask.replace('X', '1')
            or_mask = current_mask.replace('X', '0')
            current_num = long(command[1])
            and_num = long(and_mask, 2)
            or_num = long(or_mask, 2)

            # print "num: {} \n AND {}\n OR  {}".format(current_num, and_mask, or_mask)
            current_num = current_num & and_num
            current_num = current_num | or_num

            address = re.findall(r'mem\[([0-9]+)\]', command[0])[0]
            registers[address] = current_num

    return sum(registers.values())


def get_all_mask_permutations(mask):
    permutation_list = []

    if 'X' in mask:
        mask_one = mask.replace('X', '1', 1)
        permutation_list += get_all_mask_permutations(mask_one)
        mask_zero = mask.replace('X', '0', 1)
        permutation_list += get_all_mask_permutations(mask_zero)
    else:
        permutation_list += [mask]

    return permutation_list


def solve_part2(start):
    inputs = load_inputs()
    current_mask = ''
    registers = {}

    for command in inputs:
        if command[0] == 'mask':
            current_mask = command[1]
            # print "Setting mask to {}".format(command[1])
        else:
            current_num = long(command[1])
            address_list = []
            base_address = re.findall(r'mem\[([0-9]+)\]', command[0])[0]

            # use or to apply the base mask. 0/1 doesn't matter,
            # it will be forcibly overwritten later
            or_num = long(current_mask.replace('X', '1'), 2)
            this_addr = long(base_address) | or_num

            # re-instate X's from the base mask
            this_mask = '{:b}'.format(this_addr).zfill(36)
            this_mask = [x for x in this_mask]
            for ind, char in enumerate(current_mask):
                if char == 'X':
                    this_mask[ind] = 'X'
            this_mask = ''.join(this_mask)

            # generate permutations for each X combination
            mask_permutations = get_all_mask_permutations(this_mask)

            for perm in mask_permutations:
                address_list.append(perm)

            for address in address_list:
                registers[address] = current_num

    return sum(registers.values())


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
