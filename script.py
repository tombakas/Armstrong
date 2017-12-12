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

from itertools import combinations
from copy import deepcopy


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

    values = list(closures.values())
    uniques = [value for value in values if values.count(value) == 1]

    # only keep one of the closures having the same value
    for key_1, value_1 in closures.items():
        if value_1 not in uniques:
            for key_2, value_2 in closures.items():
                if value_1 == value_2:
                    if value_1 not in abridged.values():
                        abridged[key_1] == value
                    else:
                        break
        else:
            abridged[key_1] = value_1

    return abridged


def regular_armstrong(columns, closures):

    width = 5
    iterable = 2
    nr_columns = len(columns)
    entries = []

    fmt = (("{:^" + str(width) + "}|") * nr_columns)[:-1]

    print("Armstrong relation table:\n")

    print(fmt.format(*tuple(columns)))
    print("-" * ((width + 1) * nr_columns - 1))

    # empty set closure
    entries.append((0,) * nr_columns)
    entries.append((1,) * nr_columns)

    for key, value in closures.items():
        value_array = [iterable] * nr_columns
        entries.append((iterable,) * nr_columns)
        for column in columns:
            if column not in value:
                value_array[columns.index(column)] = iterable + 1
        entries.append(tuple(value_array))

        iterable += 2

    for entry in entries:
        print(fmt.format(*entry))

    print("\n* * *\n")


def strong_armstrong(columns, closures):

    nr_columns = len(columns)
    nr_entries = 2**(len(closures.keys()) + 1)

    width = 2 + len((str(bin(nr_entries - 1))))
    fmt = (("{:^" + str(width) + "}|") * nr_columns)[:-1]

    print("Strong Armstrong relation table:\n")
    print(fmt.format(*tuple(columns)))
    print("-" * ((width + 1) * nr_columns - 1))

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

    for entry in entries:
        print(fmt.format(*entry))


def main():
    f = "./dependencies.txt"

    columns = []
    dependencies = {}

    columns, dependencies = parse_file(f)
    closures = get_closures(columns, dependencies)

    good_closures_a = reduce_closures(closures, len(columns))

    regular_armstrong(columns, good_closures_a)
    strong_armstrong(columns, good_closures_a)


if __name__ == "__main__":
    main()
