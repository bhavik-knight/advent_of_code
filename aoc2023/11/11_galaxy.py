import re
from itertools import combinations
from pathlib import Path
import numpy as np


def main():
    # file_path = Path(__file__).parent.joinpath("sample.txt")
    file_path = Path(__file__).parent.joinpath("input.txt")

    print(f"Puzzle 1: {puzzle1(file_path)}")
    print(f"Puzzle 2: {puzzle2(file_path)}")
    return None


def puzzle2(file_path: list):
    positions = get_old_galaxy_positions(file_path, expansion_rate=10**6)
    # print(positions)

    distances = dict()
    for a, b in combinations(positions.values(), 2):
        d = get_manhattan_distance(a, b)
        distances[(tuple(a), tuple(b))] = d

    return sum(distances.values())


def puzzle1(file_path: list):
    positions = get_old_galaxy_positions(file_path)

    distances = dict()
    for a, b in combinations(positions.values(), 2):
        d = get_manhattan_distance(a, b)
        distances[(tuple(a), tuple(b))] = d

    return sum(distances.values())


def get_manhattan_distance(a: tuple, b: tuple) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_old_galaxy_positions(file_name: str, expansion_rate=2) -> list:
    result = list()

    # read all lines
    galaxy_number = 0
    with open(file_name) as f:
        for line in f:
            line = list(line.strip())
            for i, x in enumerate(line):
                if x != ".":
                    galaxy_number += 1
                    line[i] = galaxy_number
            result.append(line)

    # print(">>>", result)
    # for line in result:
    #     print(line)

    # bookkeeping
    count_empty_rows = 0
    old_positions = dict()

    # row exansion
    # check each lines
    for i, line in enumerate(result):
        # if whole line doesn't have any galaxy, expand
        if all(map(lambda x: x == ".", line)):
            count_empty_rows += 1
            continue

        # check for chars in a row to detect in galaxy
        for j, char in enumerate(line):
            # if galaxy is found, add the expended row position
            if char != ".":
                old_positions[char] = [i + (expansion_rate - 1) * count_empty_rows, j]
    # print("row:", old_positions)

    # column exansion
    count_empty_columns = 0
    for i, line in enumerate(np.transpose(result)):
        # print("transposed line", line)
        if all(map(lambda x: x == ".", line)):
            count_empty_columns += 1
            continue

        for j, char in enumerate(line):
            if char != ".":
                # print("...", old_positions[int(char)], i)
                old_positions[int(char)][-1] = i + (expansion_rate - 1) * count_empty_columns

    # print("col", old_positions)
    return old_positions



if __name__ == "__main__":
    main()
