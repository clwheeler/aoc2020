import collections
import time
import re
import sys
from itertools import cycle

day_str = "16"
test_input = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9"""


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
    rules = re.findall(r'([\w| ]+): (\d+)-(\d+) or (\d+)-(\d+)', inputs)
    ticket = re.search(r'your ticket:\n([\d|,]+)\n', inputs).group(1)
    nearby = re.search(r'nearby tickets:\n([\d|,\n]+)', inputs).group(1).split('\n')

    rules = [(x[0], int(x[1]), int(x[2]), int(x[3]), int(x[4])) for x in rules]
    ticket = [int(x) for x in ticket.split(',')]
    nearby = [[int(x) for x in t.split(',')] for t in nearby]
    return rules, ticket, nearby


def solve_part1(start):
    """ We could go through and do a pairwise comparison of every value
        but this is probably faster.
        Since we're just looking for values that are _never_ valid, and
        all values are in a given range, we can just construct a single list
        of all values that are valid for _some_ rule, and flag an value not
        in that list
    """
    rules, ticket, nearby  = load_inputs()
    valid_numbers = set()
    for rule in rules:
        for x in xrange(rule[1], rule[2]):
            valid_numbers.add(x)
        for x in xrange(rule[3], rule[4]):
            valid_numbers.add(x)

    invalid_numbers = []
    for ticket in nearby:
        invalid_numbers += [x for x in ticket if x not in valid_numbers]

    return sum(invalid_numbers)


def solve_part2(start):
    """
        Doing n^2 pairwise comparisons seems slow.
        If we have the index / rule mapping correct, we know that the number
        in that slot is within the rule bounds for _every_ ticket.
        This means that if any one ticket has a value outside the bounds,
        that index match that rule's field.
        For each index, we consider each rule and eliminate the ones that
        we violate. Some indexes will match match multiple rules
        However, some index will only match 1 rule. We can then progressively
        eliminate that rule from the other options, repeating until
        it condenses into a single solution.
    """
    rules, my_ticket, nearby  = load_inputs()
    # construct a single set of ranges that are valid
    valid_numbers = set()
    for rule in rules:
        for x in xrange(rule[1], rule[2]):
            valid_numbers.add(x)
        for x in xrange(rule[3], rule[4]):
            valid_numbers.add(x)

    valid_tickets = []
    for ticket in nearby:
        invalid_numbers = [x for x in ticket if x not in valid_numbers]
        if not invalid_numbers:
            valid_tickets.append(ticket)

    # for each index, look for a rule where all tickets match that rule
    possible_matches = [0] * len(ticket)
    for ind in xrange(len(ticket)):
        eligible_fields = [x for x in rules]
        for ticket in valid_tickets:
            for field in eligible_fields:
                if (field[1] <= ticket[ind] <= field[2]) or \
                   (field[3] <= ticket[ind] <= field[4]):
                    pass
                else:
                    # if the rule was violated by even 1 ticket, it can't match
                    # this index, so remove it from consideration
                    eligible_fields.remove(field)
                    # print 'Error at {} with value {}, removing {}'.format(ind, ticket[ind], field)
                    break
        possible_matches[ind] = [x for x in eligible_fields]

    # most rules will have 2 or more options. Remove duplicates
    # from where there's more than 1 until every option only has 1
    while sum([len(z) for z in possible_matches]) != len(possible_matches):
        for x in possible_matches:
            if len(x) == 1:
                this_rule = x[0]
                for y in possible_matches:
                    if len(y) > 1 and this_rule in y:
                        y.remove(this_rule)

    # for ind, val in enumerate(possible_matches):
    #     print ind, val

    # just flatten our list
    correct_indexes = [x[0] for x in possible_matches]
    departure_indexes = [correct_indexes.index(rule) for rule in correct_indexes if 'departure' in rule[0]]

    d_product = 1
    for x in departure_indexes:
        d_product = d_product * my_ticket[x]

    return d_product

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
