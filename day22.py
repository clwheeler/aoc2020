from collections import deque
import time
import re
import sys
from itertools import cycle

day_str = "22"
test_input = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""


def load_inputs(input_str=None):
    inputs = []

    if input_str:
        inputs = input_str
    else:
        with open('./inputs/day{}_input.txt'.format(day_str), 'r') as f:
            inputs = f.read()

    p1, p2 = parse_inputs(inputs)
    return p1, p2


def toInt(s):
    try:
        ival = int(s)
        return ival
    except:
        return s


def parse_inputs(inputs):
    parsed = inputs.split('\n')
    p1 = []
    p2 = []
    for x in parsed:
        if x == 'Player 1:':
            target = p1
        elif x == 'Player 2:':
            target = p2
        elif x:
            target.append(toInt(x))

    return p1, p2


def get_score(deck):
    score = zip(deck, range(len(deck), 0, -1))
    return sum([x[0] * x[1] for x in score])


def play_game(deck_deque_1, deck_deque_2):
    while len(deck_deque_1) > 0 and len(deck_deque_2) > 0:
        p1_card = deck_deque_1.popleft()
        p2_card = deck_deque_2.popleft()

        if p1_card > p2_card:
            deck_deque_1.append(p1_card)
            deck_deque_1.append(p2_card)
        else:
            deck_deque_2.append(p2_card)
            deck_deque_2.append(p1_card)

    if len(deck_deque_1) > len(deck_deque_2):
        winner = deck_deque_1
    else:
        winner = deck_deque_2

    return get_score(winner)


def solve_part1(start):
    p1, p2 = load_inputs()
    deck_deque_1 = deque(p1)
    deck_deque_2 = deque(p2)
    return play_game(deck_deque_1, deck_deque_2)


def play_game_recursive(deck_deque_1, deck_deque_2):
    # print 'Starting game: {}, {}'.format(deck_deque_1, deck_deque_2)
    game_history = []

    while len(deck_deque_1) > 0 and len(deck_deque_2) > 0:
        winner = 0
        # the score seems like a reasonable checksum?
        score_tuple = (get_score(deck_deque_1), get_score(deck_deque_2))
        if score_tuple in game_history:
            return [1], []
        game_history.append(score_tuple)

        p1_card = deck_deque_1.popleft()
        p2_card = deck_deque_2.popleft()

        if p1_card <= len(deck_deque_1) and p2_card <= len(deck_deque_2):
            p1_subdeck = list(deck_deque_1)[0:p1_card]
            p2_subdeck = list(deck_deque_2)[0:p2_card]
            d1, d2 = play_game_recursive(deque(p1_subdeck), deque(p2_subdeck))
            if len(d1) > len(d2):
                winner = 1
            else:
                winner = 2
        else:
            if p1_card > p2_card:
                winner = 1
            else:
                winner = 2

        if winner == 1:
            deck_deque_1.append(p1_card)
            deck_deque_1.append(p2_card)
        else:
            deck_deque_2.append(p2_card)
            deck_deque_2.append(p1_card)

    return deck_deque_1, deck_deque_2


def solve_part2(start):
    p1, p2 = load_inputs()
    deck_deque_1 = deque(p1)
    deck_deque_2 = deque(p2)

    r1, r2 = play_game_recursive(deck_deque_1, deck_deque_2)

    if len(r1) > len(r2):
        winner = r1
    else:
        winner = r2

    return get_score(winner)


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
