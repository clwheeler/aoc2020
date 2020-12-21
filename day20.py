from collections import defaultdict
import time
import re
import sys
from itertools import cycle
from numpy import fliplr, rot90, array

day_str = "20"


def load_inputs(test=False):
    inputs = []

    suffix = '_input.txt'

    if test:
        suffix = '_test.txt'

    with open('./inputs/day{}{}'.format(day_str, suffix), 'r') as f:
        inputs = f.read()

    parsed_test_input = parse_inputs(inputs)
    return parsed_test_input


def parse_inputs(inputs):
    """
    Represetn each tile as a numpy array
    """
    parsed = inputs.split('\n')

    result_set = dict()
    this_tile = []
    tile_id = 0
    for line in parsed:
        if 'Tile' in line:
            tile_id = re.search('Tile ([0-9]+):', line).group(1)
        elif line:
            line = line.replace('#', '1').replace('.', '0')
            split_line = [int(x) for x in line]
            this_tile.append(split_line)
        else:
            result_set[tile_id] = array(this_tile)
            this_tile = []
            tile_id = 0

    return result_set


def get_all_perms(tile):
    possibilities = []
    possibilities.append(tile[0])
    possibilities.append(rot90(tile, 1)[0])
    possibilities.append(rot90(tile, 2)[0])
    possibilities.append(rot90(tile, 3)[0])

    possibilities.append(fliplr(tile)[0])
    possibilities.append(rot90(fliplr(tile), 1)[0])
    possibilities.append(rot90(fliplr(tile), 2)[0])
    possibilities.append(rot90(fliplr(tile), 3)[0])

    return possibilities


def compare_tile(t1, t2):
    """
    Compare t2 on all sides, in order for each side. Return the tile (in the
    correct orientation) if it's a candidate.
    t1 will just compare the top row
    There might be multiple valid permutations, so lets just return a list of all
    possiibilities for now
    """
    matches = 0

    t1pos = get_all_perms(t1)
    t2pos = get_all_perms(t2)

    for t1 in t1pos:
        for t2 in t2pos:
            if t1.tolist() == t2.tolist():
                matches += 1

    return matches


def solve_part1(start):
    """
    We only need to find the 4 corners, so lets just compute all answers, and then see if
    there's a set of 4 that only have 2 matches
    """
    inputs = load_inputs(False)
    two_matches = []
    tiles = inputs.keys()
    for elem in tiles:
        matches = defaultdict(list)
        for elem2 in tiles:
            if elem != elem2 and compare_tile(inputs[elem], inputs[elem2]):
                l = matches[elem]
                l.append(elem2)

        if len(matches[elem]) == 2:
            print matches
            two_matches.append(elem)

    return reduce((lambda x, y: int(x) * int(y)), two_matches)


def solve_part2(start):
    """
    Reconstruct the image starting from an arbitrary corner.
    Since there's no orientation defined, we can pick any corner as the "top left", and
    build from there. Luckily, each tile has a unique set of neighbors, so we dont need
    to worry about multiple permutations: if it matches at all, it's correct.

    """
    inputs = load_inputs(False)
    all_matches = []
    tiles = inputs.keys()
    for elem in tiles:
        matches = defaultdict(list)
        for elem2 in tiles:
            if elem != elem2 and compare_tile(inputs[elem], inputs[elem2]):
                l = matches[elem]
                l.append(elem2)
        if matches[elem]:
            all_matches.append(matches[elem])

    # start frmo an aribtrary corner
    # find a match, rotate me so that the match is along the right side
    # fill in properly oriented match
    # repeat, for row = 1+, consider top-match and left-match

    # for eery rotations / orientation, look fot the pattern


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
