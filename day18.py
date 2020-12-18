import collections
import time
import re
import sys
from itertools import cycle

day_str = "18"
test_input = """1 + 2 * 3 + 4 * 5 + 6
2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""


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
    def parse_line(line_iter):
        """
        Use a single iterator throughout recurisions, because we only go through every
        term once
        """
        res = []

        while True:
            try:
                ind, val = line_iter.next()
                if val == '(':
                    child = parse_line(line_iter)
                    res.append(child)
                elif val == ')':
                    break
                else:
                    try:
                        res.append(int(val))
                    except:
                        res.append(val)
            except StopIteration:
                break

        return res

    parsed = inputs.split('\n')
    parsed = [parse_line(enumerate(line.replace(' ', ''))) for line in parsed]
    return parsed


def in_order_solve(terms):
    """
    Since everything is in-order, we can just walk the input string and solve
    as we go, using recursion to solve parens.
    """
    if type(terms) != list:
        return terms

    solution = 0
    terms_iter = iter(terms)

    for term in terms_iter:
        if type(term) == int or type(term) == list:
            solution += in_order_solve(term)
        else:
            # operator
            next_term = terms_iter.next()
            if term == "+":
                solution = solution + in_order_solve(next_term)
            elif term == "*":
                solution = solution * in_order_solve(next_term)
    return solution


def solve_part1(start):
    inputs = load_inputs()
    return sum([in_order_solve(eq) for eq in inputs])


def addition_first_solve(terms):
    """
    Pushing / popping from the list as we go is cleaner than the raw aggregation
    that we did above
    """
    if type(terms) != list:
        return terms

    round_2 = []

    terms_iter = iter(terms)
    for term in terms_iter:
        if term == "+":
            prv = round_2.pop()
            nxt = terms_iter.next()
            round_2.append(addition_first_solve(prv) + addition_first_solve(nxt))
        else:
            round_2.append(term)

    mult_round = []
    terms_iter = iter(round_2)
    for term in terms_iter:
        if term == "*":
            prv = mult_round.pop()
            nxt = terms_iter.next()
            mult_round.append(addition_first_solve(prv) * addition_first_solve(nxt))
        else:
            mult_round.append(term)

    return sum(mult_round)


def solve_part2(start):
    inputs = load_inputs()
    return sum([addition_first_solve(eq) for eq in inputs])


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
