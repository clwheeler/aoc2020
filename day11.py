import collections
import time
import re
import sys
from itertools import cycle

day_str = "11"
test_input = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""


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


class SeatStatus:
    OCCUPIED = '#'
    EMPTY = 'L'
    FLOOR = '.'
    OOB = 'X'


class SeatGrid:
    width = 0
    height = 0
    grid = []
    mode = ''

    def __init__(self, input_grid, mode='nearest'):
        self.grid = [[x for x in row] for row in input_grid]
        self.height = len(input_grid)
        self.width = len(input_grid[0])
        self.mode = mode

    def count(self, status):
        return sum([len([x for x in row if x == status]) for row in self.grid])

    def print_grid(self):
        print "====================="
        for row in self.grid:
            print ''.join(row)

    # off edges count as non-occupied
    def getElemAt(self, x, y):
        if x >= self.width or y >= self.height or x < 0 or y < 0:
            return SeatStatus.OOB
        return self.grid[y][x]

    def getNeighbors(self, x, y):
        neighborPos = [(x-1, y-1), (x, y-1), (x+1, y-1), (x+1, y), (x+1, y+1), (x, y+1), (x-1, y+1), (x-1, y)]
        neighbors = [self.getElemAt(a[0], a[1]) for a in neighborPos]
        return neighbors

    def getVisibleNeighbors(self, x, y):
        def findFirstInDirection(x, y, dir_tuple):
            seen = '.'
            offset = (0, 0)
            while(seen == '.'):
                offset = (offset[0] + dir_tuple[0], offset[1] + dir_tuple[1])
                seen = self.getElemAt(x + offset[0], y + offset[1])
            return seen

        directions = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
        neighbors = []
        for direction in directions:
            found = findFirstInDirection(x, y, direction)
            neighbors.append(found)
        return neighbors

    def tick(self):
        grid_copy = [[x for x in row] for row in self.grid]
        changed = False
        for x in xrange(self.width):
            for y in xrange(self.height):
                this_elem = self.getElemAt(x, y)
                neighbors = []
                max_neighbors = 4
                if self.mode == 'first_visible':
                    neighbors = self.getVisibleNeighbors(x, y)
                    max_neighbors = 5
                else:
                    neighbors = self.getNeighbors(x, y)
                # print x, y, this_elem, ''.join(neighbors), neighbors.count('#')
                neighbor_count = neighbors.count('#')
                if this_elem == SeatStatus.EMPTY and neighbor_count == 0:
                    changed = True
                    grid_copy[y][x] = SeatStatus.OCCUPIED
                if this_elem == SeatStatus.OCCUPIED and neighbor_count >= max_neighbors:
                    changed = True
                    grid_copy[y][x] = SeatStatus.EMPTY
        self.grid = [[x for x in row] for row in grid_copy]

        return changed


def solve_part1(start):
    input_grid = load_inputs()
    seat_grid = SeatGrid(input_grid)

    tick_count = 0
    while(seat_grid.tick()):
        tick_count += 1

    return '{} seats after {} generations.'.format(seat_grid.count(SeatStatus.OCCUPIED), tick_count)


def solve_part2(start):
    input_grid = load_inputs()
    seat_grid = SeatGrid(input_grid, 'first_visible')

    tick_count = 0
    while(seat_grid.tick()):
        tick_count += 1

    return '{} seats after {} generations.'.format(seat_grid.count(SeatStatus.OCCUPIED), tick_count)


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
