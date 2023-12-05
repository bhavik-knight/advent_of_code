import re
from pathlib import Path
from typing import List


def main():
    # file_path = Path(__file__).parent.joinpath("3_1_sample_input.txt")
    file_path = Path(__file__).parent.joinpath("3_1_input.txt")

    lines = get_lines(file_path)
    part_numbers = get_part_numbers_new(lines)
    print(f"Part numbers: {part_numbers}")

    # part 1
    only_numbers = list(map(lambda x: x[1], part_numbers))
    print(f"Only numbers: {only_numbers}")
    total = sum(flatten_list(map(lambda x: x[1], part_numbers)))
    print(f"Total: {total}")
    print()

    # part 2
    # for only gear ratio we need only * symbol having 2 number around it
    gear_ratio_list = list(filter(lambda x: x[0] == "*" and len(x[1]) == 2, part_numbers))
    print(f"Gear ratio numbers: {gear_ratio_list}")

    # extract only numbers
    only_gear_ratio_numbers = list(map(lambda x: x[1], gear_ratio_list))
    print(f"Only numbers: {only_gear_ratio_numbers}")

    # get the desired sum
    total = sum(map(lambda x: x[0] * x[1], only_gear_ratio_numbers))
    print(f"Total: {total}")
    return None


def get_part_numbers_new(lines: str) -> List[int]:
    # to map symbol to numbers
    numbers: [(str, int)] = list()

    # from each line extract sybmol and numbers surrounding it
    for line_number, line in enumerate(lines):
        # find all non digit and non dot characters
        matches = re.finditer(r"[^\d\.]+", line.strip())

        # go through each match
        for m in matches:
            # extract index and symbol from the match
            index = m.start()
            symbol = line[index]

            # find all the numbers for the current line
            get_numbers_result = find_numbers(index, line_number, lines)

            # since we have 3 lines to look for numbers, dictionary is returned for each of them
            # extract the value for each line, if value is empty we don't need it
            # flatten the list of values (because each value itself is a list)
            all_found_values = flatten_list(list(value for value in get_numbers_result.values() if value))

            # map symbol to found numbers
            numbers.append((symbol, all_found_values))
            # print("found", line_number, index, symbol, all_found_values)

    return numbers


def find_numbers(index: int, line_number: int, lines: list) -> List[int]:
    numbers: dict = dict()

    # if first or last line
    if line_number == 0 or line_number == len(lines) - 1:
        current_line = lines[line_number]
        return {"First/Last": current_line_numbers(index, current_line)}

    prv_line = lines[line_number - 1]
    prv_numbers = prv_nxt_line_numbers(index, prv_line)
    numbers["prv"] = prv_numbers

    cur_line = lines[line_number]
    cur_numbers = current_line_numbers(index, cur_line)
    numbers["cur"] = cur_numbers

    nxt_line = lines[line_number + 1]
    nxt_numbers = prv_nxt_line_numbers(index, nxt_line)
    numbers["nxt"] = nxt_numbers

    return numbers


def prv_nxt_line_numbers(index: int, line: int) -> List[int]:
    numbers = list()

    # if current char is a digit, we must find start and end of this digit
    if line[index].isdigit():
        # find the start of digit
        prv = index - 1
        while prv >= 0:
            if line[prv].isdigit():
                prv -= 1
            else:
                break

        # find the end of digit
        nxt = index + 1
        while nxt < len(line) - 1:
            if line[nxt].isdigit():
                nxt += 1
            else:
                break
        numbers.append(int(line[prv + 1 : nxt]))

    # otherwise, number is at either the entirely on the left or enitrely on the right
    # for this we can use chec current_line_numbers function, as it does exactly this task
    else:
        numbers.extend(current_line_numbers(index, line))

    return numbers


def current_line_numbers(index: int, line: int) -> List[int]:
    # we can have 2 numbers, one on the left and one on the right for the sybmol in the current line
    numbers = list()

    prv_number, nxt_number = None, None

    # find the number on the left
    number_found = False
    prv = index - 1
    while prv >= 0:
        if line[prv].isdigit():
            number_found = True
            prv -= 1
        else:
            break

    if number_found:
        prv_number = line[prv + 1 : index]
        numbers.append(int(prv_number))

    # find the number on the right
    number_found = False
    nxt = index + 1
    while nxt < len(line):
        if line[nxt].isdigit():
            number_found = True
            nxt += 1
        else:
            break

    if number_found:
        nxt_number = line[index + 1 : nxt]
        numbers.append(int(nxt_number))

    return numbers


def flatten_list(l: list) -> List[int]:
    # if list is empty nothing to flatten
    if not l:
        return []

    # otherwise start with an empty list
    result = []

    # go through each item in the list
    for item in l:
        # if item is a list itself, we need to flatten it again
        # extend the flattened list to the result
        if isinstance(item, list):
            result.extend(flatten_list(item))
        # otherwise append the item to the result
        else:
            result.append(item)
    return result


def get_lines(file_name: str) -> List[str]:
    with open(file_name, "r") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
