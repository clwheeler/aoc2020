from collections import defaultdict
import time
import re
import sys
from itertools import cycle

day_str = "21"
test_input = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""


class IngredientList():

    ingredients = []
    allergens = []

    def __init__(self, string):
        self.ingredients = string.split(' (contains')[0].split(' ')
        self.allergens = [m[1] for m in re.findall(r'(contains |, )(\w+)', string)]

    def __str__(self):
        return "Indredients: {}\nAllergens{}".format(self.ingredients, self.allergens)

    def get_allergens(self):
        return self.allergens

    def get_ingredients(self):
        return self.ingredients

    # def getContains

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
    ing_list = [IngredientList(x) for x in parsed]
    return ing_list


def get_all_ingredients(all_ilists):
    all_ingredients = set()

    for ilist in all_ilists:
        this_ingredients = ilist.get_ingredients()
        all_ingredients.update(this_ingredients)

    return all_ingredients


def get_allergen_map(all_ilists):
    # maps alergen to potential ingredients
    allergen_map = dict()

    for ilist in all_ilists:
        this_allergens = ilist.get_allergens()
        this_ingredients = ilist.get_ingredients()

        for allergen in this_allergens:
            possible_allergens = allergen_map.get(allergen, this_ingredients)
            intrsct = [a for a in possible_allergens if a in this_ingredients]
            allergen_map[allergen] = intrsct

    return allergen_map


def solve_part1(start):
    """
    Compile a list of all allergens
    For each allergeg, find all ingredient lists that reference it
    Get an intersection of those lists to find all candidates for that allergen
    Return all ingredients not in the allergen list
    """
    all_ilists = load_inputs()

    allergen_map = get_allergen_map(all_ilists)
    all_ingredients = get_all_ingredients(all_ilists)

    all_potential_bad_ingredients = set()

    for l in allergen_map.values():
        all_potential_bad_ingredients.update(l)

    safe_ingredients = [a for a in all_ingredients if a not in all_potential_bad_ingredients]

    safe_ingred_count = 0
    for ilist in all_ilists:
        this_ingredients = ilist.get_ingredients()
        this_safe_ingredients = [a for a in this_ingredients if a in safe_ingredients]
        safe_ingred_count += len(this_safe_ingredients)

    return safe_ingred_count


def solve_part2(start):
    all_ilists = load_inputs()

    allergen_map = get_allergen_map(all_ilists)

    unique_map = dict()

    for key in cycle(allergen_map.keys()):
        this_value = allergen_map[key]
        for known_ing in unique_map.values():
            if known_ing in this_value:
                this_value.remove(known_ing)
        allergen_map[key] = this_value
        if len(this_value) == 1:
            unique_map[key] = allergen_map[key][0]

        if len(unique_map.keys()) == len(allergen_map.keys()):
            break

    sorted_allergens = sorted(unique_map.keys())
    sorted_ings = [unique_map[x] for x in sorted_allergens]

    return ','.join(sorted_ings)

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
