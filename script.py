#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    File name: strong_arms.py
    Author: Tomas Tombakas
    Email: tomas@tombakas.com
    Date created: 11/12/2017
"""

import re
import string

from collections import OrderedDict

from pprint import pprint
from itertools import combinations
from itertools import tee

from functools import reduce

from copy import deepcopy


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def parse_file(f):

    columns = []
    dependencies = {}

    with open(f, "r") as f:
        for line in f:
            if "R =" in line:
                for item in re.split(",|\(|\)", line.split("=")[1]):
                    item = item.strip()
                    if item != "":
                        if item in string.ascii_uppercase:
                            columns.append(item)

            if "F =" in line:
                for item in re.split(",|\{|\}", line.split("=")[1]):
                    item = item.strip()
                    if item != "":
                        key, value = tuple(re.split("->", item))
                        dependencies[key] = dependencies.get(key, "") + value

    return columns, dependencies


def get_combinations(columns):
    combs = []

    for n in range(1, len(columns)):
        for c in combinations(columns, n):
            combs.append("".join(c))

    return combs


def get_closures(columns, dependencies):
    closures_a = {}
    closures_b = {}

    combs = get_combinations(columns)

    for comb in combs:
        closures_a[comb] = comb

    while True:
        closures_b = deepcopy(closures_a)

        for left_side, right_side in closures_a.items():

            for key, value in dependencies.items():
                if key in right_side:
                    if value not in right_side:
                        closures_a[left_side] += value

        if closures_a == closures_b:
            break

    for key, value in closures_a.items():
        closures_a[key] = "".join(sorted(value))

    return closures_a


def reduce_closures(closures, n):
    abridged = {}

    # Remove closures that are superkeys
    for key, value in deepcopy(closures).items():
        if len(value) >= n:
            del closures[key]

    # only keep one of the closures having the same value
    for key, value in closures.items():
        if value not in abridged.values():
            abridged[key] = value

    return abridged


def regular_armstrong(columns, closures, print_to_screen=True):

    iterable = 2
    nr_columns = len(columns)
    entries = []
    armstrong = {}
    tex_armstrong = OrderedDict()

    # empty set closure
    entries.append([0] * nr_columns)
    entries.append([1] * nr_columns)

    tex_armstrong["0"] = [
        ["1_∅"] * nr_columns,
        ["0_∅"] * nr_columns
    ]

    for key, value in closures.items():
        tex_entries = []
        tex_value_array = []

        value_array = [iterable] * nr_columns
        entries.append(deepcopy(value_array))

        for column in columns:
            tex_value_array.append("1_" + key)
        tex_entries.append(deepcopy(tex_value_array))

        for column in columns:
            if column not in value:
                value_array[columns.index(column)] = iterable + 1
                tex_value_array[columns.index(column)] = "0_" + key
        entries.append(value_array)
        tex_entries.append(tex_value_array)

        tex_armstrong[key] = tex_entries
        iterable += 2

    width = len(str(iterable)) + 4
    fmt = (("{:^" + str(width) + "}|") * nr_columns)[:-1]

    armstrong["name"] = "Armstrong relation table"
    armstrong["width"] = width
    armstrong["format"] = fmt
    armstrong["columns"] = tuple(columns)
    armstrong["entries"] = entries

    return armstrong, tex_armstrong


def strong_armstrong_paul(columns, closures, print_to_screen=True):

    nr_columns = len(columns)
    nr_entries = 2**(len(closures.keys()) + 1)
    width = 2 + len((str(bin(nr_entries - 1))))

    strong_armstrong = {}

    fmt = (("{:^" + str(width) + "}|") * nr_columns)[:-1]

    entries = [[""] * nr_columns for a in range(nr_entries)]

    for i in range(nr_entries):
        for j in range(nr_columns):
            if i < nr_entries / 2:
                entries[i][j] += "0"
            else:
                entries[i][j] += "1"

    interval = nr_entries / 4
    switch = False
    for key, value in closures.items():
        for n, entry in enumerate(entries):
            for i in range(nr_columns):
                if columns[i] in key:
                    entry[i] += "0"
                else:
                    if not switch:
                        entry[i] += "0"
                    else:
                        entry[i] += "1"
            if (n + 1) % interval == 0:
                switch = not switch
        interval /= 2
        switch = False

    strong_armstrong["name"] = "Strong Armstrong relation table"
    strong_armstrong["width"] = width
    strong_armstrong["format"] = fmt
    strong_armstrong["columns"] = tuple(columns)
    strong_armstrong["entries"] = entries

    return strong_armstrong


def strong_armstrong_product(relations):
    lists = [relations[key] for key in relations.keys()]

    def meld(a, b):
        concatenated = []

        for item_1 in a:
            for item_2 in b:
                concatenated.append(
                    ["".join(s) for s in zip(item_1, item_2)]
                )
            pprint(concatenated)
        return concatenated

    return reduce(meld, lists)


def print_relation(relation_dict):
    print("-" * (len(relation_dict["name"]) + 1))
    print(relation_dict["name"] + ":\n")
    print(relation_dict["format"].format(*relation_dict["columns"]))
    print("-" * ((relation_dict["width"] + 1) * len(relation_dict["columns"]) - 1))

    for entry in relation_dict["entries"]:
        print(relation_dict["format"].format(*entry))
    return


def main():
    f = "./dependencies.txt"

    columns = []
    dependencies = {}

    columns, dependencies = parse_file(f)
    closures = get_closures(columns, dependencies)

    abridged_closures = reduce_closures(closures, len(columns))

    armstrong, tex_armstrong = regular_armstrong(columns, abridged_closures, False)
    strong_armstrong = strong_armstrong_paul(columns, abridged_closures)

    print_relation(armstrong)
    print_relation(strong_armstrong)


if __name__ == "__main__":
    main()
