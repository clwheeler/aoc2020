import collections
import time
import re
import sys
from itertools import cycle

day_str = "12"
test_input = """F10
N3
F7
R90
F11"""


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





class Mover:
    pos = (0, 0)
    facing = 0

    def __init__(self):
        pass

    def get_pos(self):
        return self.pos

    def turn(self, dir, deg):
        # pos = clockwise
        new_facing = 0
        if dir == 'L':
            new_facing = self.facing - deg
        elif dir == 'R':
            new_facing = self.facing + deg

        self.facing = new_facing % 360

    def move(self, dir, val):
        offset = (0, 0)
        if dir == 'N':
            offset = (0, -1)
        elif dir == 'E':
            offset = (1, 0)
        elif dir == 'W':
            offset = (-1, 0)
        elif dir == 'S':
            offset = (0, 1)
        else :
            # dir == F
            index = self.facing / 90
            offsets = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            offset = offsets[index]

        new_pos = (self.pos[0] + offset[0] * val, self.pos[1] + offset[1] * val)
        self.pos = new_pos

def solve_part1(start):
    inputs = load_inputs()
    mover = Mover()
    for i in inputs:
        if i[0] in ['L', 'R']:
            mover.turn(i[0], int(i[1:]))
        else:
            mover.move(i[0], int(i[1:]))

    return abs(mover.get_pos()[0]) + abs(mover.get_pos()[1])


class FollowMover:
    pos = (0, 0)
    waypoint = (10, -1)

    def __init__(self):
        pass

    def get_pos(self):
        return self.pos

    def rotate_waypoint(self, dir, deg):
        # rotation around the origin:
        # x = xcos(a) - ysin(a)
        # y = xsin(a) + ycos(a)
        # sin / cos lookups
        sin = {90: 1, 180: 0, 270: -1}
        cos = {90: 0, 180: -1, 270: 0}

        # flip sign on sin for neg numbers.
        # cos(180)/cos(-180) doesn't flip sign in this range
        if dir == 'L':
            newx = self.waypoint[0]*cos[deg] - self.waypoint[1]*-sin[deg]
            newy = self.waypoint[0]*-sin[deg] + self.waypoint[1]*cos[deg]
        elif dir == 'R':
            newx = self.waypoint[0]*cos[deg] - self.waypoint[1]*sin[deg]
            newy = self.waypoint[0]*sin[deg] + self.waypoint[1]*cos[deg]

        self.waypoint = (newx, newy)

    def move_waypoint(self, dir, val):
        # waypoint co-ords relative to this pos
        offset = (0, 0)
        if dir == 'N':
            offset = (0, -val)
        elif dir == 'E':
            offset = (val, 0)
        elif dir == 'W':
            offset = (-val, 0)
        elif dir == 'S':
            offset = (0, val)

        self.waypoint = (self.waypoint[0] + offset[0], self.waypoint[1] + offset[1])

    def chase(self, val):
        # move towards waypoint val times
        new_pos = (self.pos[0] + self.waypoint[0] * val, self.pos[1] + self.waypoint[1] * val)
        self.pos = new_pos


def solve_part2(start):
    inputs = load_inputs()
    mover = FollowMover()
    for i in inputs:
        if i[0] in ['L', 'R']:
            mover.rotate_waypoint(i[0], int(i[1:]))
        elif i[0] in ['N', 'E', 'W', 'S']:
            mover.move_waypoint(i[0], int(i[1:]))
        else:
            mover.chase(int(i[1:]))

    return abs(mover.get_pos()[0]) + abs(mover.get_pos()[1])


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
