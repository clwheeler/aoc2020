import time
import re

day_str = "04"


def load_inputs():
    inputs = []
    with open('./inputs/day{}_input.txt'.format(day_str), 'r') as f:
        inputs = f.read()
    parsed = inputs.split('\n\n')
    parsed = [x.replace('\n', ' ') for x in parsed]
    return parsed


def solve_part1(start):
    """
    Python list comprehensions are magic.
    """
    inputs = load_inputs()
    required_attrs = ['ecl', 'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    result = [x for x in inputs if all([attr in x for attr in required_attrs])]
    return len(result)


def validate_hgt(x):
    """
    If cm, the number must be at least 150 and at most 193.
    If in, the number must be at least 59 and at most 76.

    This could be a lambda, but its kinda long
    """
    if x[-2:] == 'cm' and int(x[:-2]) >= 150 and int(x[:-2]) <= 193:
        return True
    if x[-2:] == 'in' and int(x[:-2]) >= 59 and int(x[:-2]) <= 76:
        return True
    return False


def solve_part2(start):
    inputs = load_inputs()
    required_attrs = {
        'byr': lambda x: len(x) == 4 and int(x) >= 1920 and int(x) <= 2002,
        'iyr': lambda x: len(x) == 4 and int(x) >= 2010 and int(x) <= 2020,
        'eyr': lambda x: len(x) == 4 and int(x) >= 2020 and int(x) <= 2030,
        'hgt': validate_hgt,
        'hcl': lambda x: re.match(r'^#[0-9a-f]{6}$', x) is not None,
        'ecl': lambda x: x in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
        'pid': lambda x: re.match(r'^[0-9]{9}$', x) is not None,
    }
    valid = 0

    has_all_fields = [x for x in inputs if all([attr in x for attr in required_attrs.keys()])]

    for passport in has_all_fields:
        fields = passport.split(' ')
        field_success = []
        for field in fields:
            attr, value = field.split(":")
            if attr in required_attrs.keys():
                success = required_attrs[attr](value)
                field_success.append(success)
        if all(field_success):
            valid += 1
    return valid


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
