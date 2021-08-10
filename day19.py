import collections
import time
import re
import sys
from itertools import cycle

day_str = "19"
test_input = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""



def toInt(s):
    try:
        ival = int(s)
        return ival
    except:
        return s

def load_inputs(input_str=None):
    inputs = []

    if input_str:
        inputs = input_str
    else:
        with open('./inputs/day{}_input.txt'.format(day_str), 'r') as f:
            inputs = f.read()

    rules, messages = parse_inputs(inputs)
    return rules, messages


def parse_inputs(inputs):
    """
    Rules are all of the type A -> BC or A -> a
    Basically, in CNF already
    """
    parsed = inputs.split('\n')
    messages = []

    for line in parsed:
        if ':' in line:
            rule_num = int(line.split(':')[0])
            rules = line.split(':')[1].strip().replace('"', '').split('|')
            rules = [x.strip().split(' ') for x in rules]
            all_rules[rule_num] = [[toInt(y) for y in x] for x in rules]
        else:
            messages.append(line)

    ALL_RULES = all_rules

    return messages


def string_matches_rule(rule_index, string):
    for rule in ALL_RULES[rule_index]:
        string_matches_rule(rule.idx, string[1:])


ALL_RULES = dict()

def solve_part1(start):
    """
    Walk through the characters in the message
    for each char, build a list of potentail rule paths that are being followed
    buitld path-tree
    If this path stops being viable, prune this branch
    Pruning pro
    """

    messages = load_inputs(test_input)
    for message in messages:
        possible_rule_paths = []
        string_matches_rule(0, message)
        for char in message:
            for rule in rules:
                # walk through a
                pass
                string_matches_rule(0, message)


def solve_part2(start):
    # inputs = load_inputs(test_input)
    return "TODO"


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
