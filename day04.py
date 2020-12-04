import collections
import time
import re
import sys
from itertools import cycle

day_str = "04"
test_input = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""

invalid_test =   """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007"""

valid_test = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"""


def load_inputs():
    inputs = []
    with open('./inputs/day{}_input.txt'.format(day_str), 'r') as f:
        inputs = f.read()
    inputs = parse_inputs(inputs)
    return inputs


def load_test_inputs():
    parsed_test_input = parse_inputs(valid_test)
    return parsed_test_input


def parse_inputs(inputs):
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
