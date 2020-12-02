import collections
import time
import re
import sys
from itertools import cycle


def load_inputs(day_str):
    inputs = []
    with open('./inputs/day{}_input.txt'.format(day_str), 'r') as f:
        for line in f:
            inputs.append(line.rstrip())
    inputs = parse_inputs(inputs)
    return inputs


def parse_inputs(inputs):
    parsed = [x.split(' ') for x in inputs]
    return parsed

def load_test_inputs(_):
    test_input = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc""".splitlines()
    return parse_inputs(test_input)


def solve_part1(day, start):
    inputs = load_inputs(day)
    valid = 0
    for x in inputs:
        (rule, letter, pwd) = x
        letter = letter.replace(':', '')
        rule_min, rule_max = rule.split('-')
        rule_min = int(rule_min)
        rule_max = int(rule_max)

        if pwd.count(letter) >= rule_min and pwd.count(letter) <= rule_max:
            valid += 1

    return valid


def solve_part2(day, start):
    inputs = load_inputs(day)
    valid = 0
    for x in inputs:
        (rule, letter, pwd) = x
        letter = letter.replace(':', '')
        rule_min, rule_max = rule.split('-')
        rule_min = int(rule_min)
        rule_max = int(rule_max)

        if pwd[rule_min-1] == letter and pwd[rule_max-1] != letter:
            valid += 1
        elif pwd[rule_min-1] != letter and pwd[rule_max-1] == letter:
            valid += 1

    return valid


def run():

    day = "02"

    start_time = time.time()
    print "Part 1:"
    print solve_part1(day, 0)
    print "Runtime: {} seconds".format(time.time() - start_time)

    start_time = time.time()
    print "Part 2:"
    print solve_part2(day, 0)
    print "Runtime: {} seconds".format(time.time() - start_time)

run()
