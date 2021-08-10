from collections import deque
import time
import re
import sys
from itertools import cycle

day_str = "00"
test_input = """x"""


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


def solve_part1(input_str, turns, cup_count=9):
    """
    Our old friend deque is ideal for circular lists
    """
    inputs = [int(x) for x in input_str]
    while len(inputs) < cup_count:
        inputs.append(len(inputs)+1)

    circle = deque(inputs)
    MAX_VAL = max(inputs)

    print circle

    for x in xrange(turns):
        hand = []
        current = circle[0]
        circle.rotate(-1)
        # pull next 3
        for x in xrange(3):
            hand.append(circle.popleft())
        # print "Hand: {}".format(hand)
        nxt = circle[0]
        # insert: rotate until in proper position, extend
        target = current - 1
        if target <= 0:
            target = MAX_VAL
        while target in hand:
            target = target - 1
            if target <= 0:
                target = MAX_VAL
        # print "Target: {}".format(target)
        while circle[0] != target:
            circle.rotate(-1)
        circle.rotate(-1)
        circle.extend(hand)
        while circle[0] != nxt:
            circle.rotate(-1)

    while circle[0] != 1:
        circle.rotate()

    sol = [str(x) for x in list(circle)[0:9]]
    return ''.join(sol)


class CircleArray():
    next_values_array = []

    def __init__(self, inputs, size):
        while len(inputs) < size:
            inputs.append(len(inputs)+1)

        # print inputs

        circle_arr = [0] * (size+1)
        for ind, elem in enumerate(inputs):
            nxt = (ind+1) % size
            # print "{} => {}".format(elem, inputs[nxt])
            circle_arr[elem] = inputs[nxt]
        self.next_values_array = circle_arr

    def getState(self, head):
        circle = [head]
        for x in xrange(20):
            next_val = self.next_values_array[circle[-1]]
            if next_val == head:
                break
            circle.append(next_val)
        return circle

    def getNextValue(self, value):
        return self.next_values_array[value]

    def removeElementsAfterValue(self, value, count):
        """
        Returns a sequence that was removed
        """
        old_nxt = []
        this_value = value
        for x in xrange(count):
            old_nxt.append(self.next_values_array[this_value])
            this_value = old_nxt[-1]
        # print "removing {}".format(old_nxt)
        self.next_values_array[value] = self.next_values_array[old_nxt[-1]]
        return old_nxt

    def insertElementsAfter(self, value, to_insert):
        """
        Assumes to_insert is a contiguous set of elements
        """
        # print "inserting {}".format(to_insert)
        old_nxt = self.next_values_array[value]
        new_last = to_insert[-1]
        self.next_values_array[value] = to_insert[0]
        self.next_values_array[new_last] = old_nxt


def solve_part2(input_str, turns, cup_count=9):
    """
    This is super slow, because even though rotate is O(1), we're doing 2*n of them,
    1 to find the destination, and then 1 to rotate back...
    Python 2.7 doens't have deque.index o_O
    Because we only ever search clockwise, we can basically do this with a
    singly linked list, where each element has a value and a pointer to the
    next (clockwise) element
    We also keep an array where the arr[i] = element with value i
    Removing our elements is rearranging pointers,
    looking up the Destination is array lookup
    Re-insertion is rerranging pointers
    Since value = index, and there's only 1 data point, this could be just a
    an array of "next number" values
    """
    inputs = [int(x) for x in input_str]
    head_value = inputs[0]

    # print inputs
    circle = CircleArray(inputs, cup_count)
    circle.getState(head_value)

    MAX_VAL = len(inputs)

    for x in xrange(turns):
        # print '\nTurn', x
        hand = circle.removeElementsAfterValue(head_value, 3)
        # circle.printState(head_value)

        target = head_value - 1
        if target <= 0:
            target = MAX_VAL
        while target in hand:
            target = target - 1
            if target <= 0:
                target = MAX_VAL

        # print "Target: {}".format(target)

        circle.insertElementsAfter(target, hand)
        # circle.printState(head_value)
        head_value = circle.getNextValue(head_value)
        # circle.printState(head_value)

    # print circle.getState(head_value)
    end_state = circle.getState(1)
    return end_state[1] * end_state[2]
    # sol = [str(x) for x in list(circle_arr)[0:9]]
    # return ''.join(sol)


def run():

    start_time = time.time()
    print "Part 1:"
    print solve_part1("364289715", 100, 9)
    print "Runtime: {} seconds".format(time.time() - start_time)

    start_time = time.time()
    print "Part 2:"
    print solve_part2("364289715", 10000000, 1000000)

    print "Runtime: {} seconds".format(time.time() - start_time)

run()
