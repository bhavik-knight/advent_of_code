"""
AOC 2024
Day 2: Red-Nosed Reports
Coded by: Bhavik Knight
"""

from collections import Counter, defaultdict
from itertools import compress
from time import perf_counter


def main():

    files = ["test_input.txt", "input.txt"]
    for file in files:
        print("=" * 80)
        reports = parse_input(file)

        total_part1, total_part2 = 0, 0
        memory: dict[tuple, bool] = {}

        for i, report in enumerate(reports, 1):
            result = analyze_report(report, len(report), dampener=False)
            print(f"Part1: Report{i} = {report} :=> {result}")

            total_part1 += int(result)
            memory[tuple(report)] = result

        print("-" * 50)

        for i, report in enumerate(reports, 1):
            if memory[tuple(report)]:
                total_part2 += 1
                continue
            result = analyze_report(report, len(report), dampener=True, memory=memory)
            print(f"Part2: Report{i} = {report} :=> {result}")
            total_part2 += int(result)

        print("-" * 50)

        print(f"Part1: {total_part1}")
        print(f"Part2: {total_part2}")
        print("=" * 80)


def main_old():
    files = ["test_input.txt", "input.txt"]

    for file in files[:1]:
        reports = parse_input(file)
        # print(f"Reports: {reports}")
        # reports = [[78, 81, 78, 80, 81, 83, 85, 83]]

        total_part1, total_part2 = 0, 0
        # to store the result of the part1
        memory: dict[tuple, bool] = {}
        for i, report in enumerate(reports, 1):
            result = analyze_report_(report, len(report), False)
            # print(
            #     f"Part 1: => Report {i}: {report} range: => {is_difference_in_range(report, False)}\t"
            #     + f"^: => {is_strictly_increasing(report)}\t"
            #     + f"v: => {is_strictly_decreasing(report)}\t==> {result}"
            # )
            total_part1 += int(result)
            memory[tuple(report)] = result

        for i, report in enumerate(reports, 1):
            if memory[tuple(report)]:
                continue
            result = analyze_report(report, len(report), True, memory)
            print(
                f"Part 2: => Report {i} {report}\t"
                + f"range: => {is_difference_in_range(report, True)}"
                + f"^: => {is_strictly_increasing(report)}"
                + f"v: => {is_strictly_decreasing(report)}==> {result}"
            )
            total_part2 += int(result)

        print("-" * 50)
        print(f"Part 1:=> Number of safe reports: {total_part1}")
        print(f"Part 2:=> Number of safe reports: {total_part2}")
        print("\v")
        print("=" * 80)


def analyze_report(report: list[int], length: int, dampener: bool = True, memory: dict = {}) -> bool:
    if not dampener:
        result_diff = is_diff(report)
        result_inc_dec = is_inc_dec(report, length)
        print(f"\t{report} :=> RD: {result_diff}, RID: {result_inc_dec} ==> {result_diff and result_inc_dec}")
        return result_diff and result_inc_dec

    associated_report_result = {}
    for report in associated_report(report):
        ld = get_level_diff(report)
        tc = get_tolerance_count(ld)
        nrc, prc, zrc = get_npz_count(ld)
        print(f"AR: {report} => TC = {tc}, (-, +, 0) = {nrc, prc, zrc}")

        if nrc > 1 and prc > 0 or nrc > 0 and prc > 1 or zrc > 0 or tc > 0:
            associated_report_result[tuple(report)] = False
        else:
            associated_report_result[tuple(report)] = True

    print(f"\t {report} AR: {associated_report_result}")
    return any(associated_report_result.values())


def parse_input(file_name: str) -> list[list[int]]:
    with open(file_name, "r", encoding="UTF-8") as f:
        lines = [line.strip() for line in f.readlines()]

    result: list = [list(map(int, line.split())) for line in lines]
    return result


def associated_report(report: list[int]) -> list[list[int]]:
    lists = [report[:i] + report[i + 1 :] for i in range(len(report))]
    return lists


def get_level_diff(report: list[int]) -> list[int]:
    return [y - x for x, y in zip(report[:-1], report[1:])]


def get_npz_count(numbers: list[int]) -> list[int]:
    neg_count = sum(map(lambda x: x < 0, numbers))
    pos_count = sum(map(lambda x: x > 0, numbers))
    zero_count = sum(map(lambda x: x == 0, numbers))
    return [neg_count, pos_count, zero_count]


def get_tolerance_count(numbers: list[int]) -> int:
    return sum(map(lambda x: not 1 <= abs(x) <= 3, numbers))


def is_diff(report: list[int]) -> bool:
    ld = get_level_diff(report)
    tolerance_counter = get_tolerance_count(ld)
    # print(f"TC: => {report}: {tolerance_counter}")
    return tolerance_counter == 0


def is_inc_dec(report: list[int], length: int) -> bool:
    level_diff = get_level_diff(report)
    nc, pc, zc = get_npz_count(level_diff)
    # print(f" OG (-, +, 0): ({nc, pc, zc})")

    if nc >= 1 and pc >= 1 or zc > 0:
        return False
    if nc >= 1 and pc == 0 and zc == 0 or nc == 0 and pc >= 1 or zc == 0:
        return True


def analyze_report_(report: list[int], length: int, dampener: bool = False, memory: dict = {}) -> bool:
    # because at most one fault is tolerated
    if length - len(report) > 1:
        return False

    if memory.get(tuple(memory)):
        return True

    # check if start and end are equal, if they're move the start to the right
    start_index = 0
    if report[start_index] == report[-1]:
        start_index += 1

    # check if the levels difference are within the range [1, 3]
    is_in_range = is_difference_in_range(report, dampener)

    # check if the report is strictly increasing or strictly decreasing
    is_strictly_inc = is_strictly_increasing(report)
    is_strictly_dec = is_strictly_increasing(report)

    return is_in_range


def is_difference_in_range(numbers: list[int], dampener: bool) -> bool:
    if len(numbers) < 2:
        return False

    if len(numbers) < 3:
        return 1 <= numbers[-1] - numbers[0] <= 3 if not dampener else True

    tolerance_count = 0
    cur_index = 0
    visited_numbers = set()
    for nxt_index in range(1, len(numbers)):
        # find the difference between adjacent elements
        cur = numbers[cur_index]
        nxt = numbers[nxt_index]

        if cur in visited_numbers:
            tolerance_count += 1

        if nxt in visited_numbers:
            tolerance_count += 1
            nxt_index += 1
            nxt = numbers[nxt_index]

        difference = nxt - cur
        visited_numbers.add(cur)
        # difference not in the range [1,3]
        if not 1 <= abs(difference) <= 3:
            # increase the tolerance_count
            tolerance_count += 1

            # if dampener is allowed and tolerance_count is more than 1 => unsafe report
            if dampener and tolerance_count > 1:
                return False

            # if dampener is not allowed, and not in the range => unsafe report
            if not dampener:
                return False

        # difference in the range [1,3]
        else:
            cur_index = nxt_index

    return True


def is_strictly_increasing(numbers: list[int]) -> bool:
    for prev, curr in zip(numbers[:-1], numbers[1:]):
        if curr - prev <= 0:
            return False
    return True


def is_strictly_decreasing(numbers: list[int]) -> bool:
    for prev, curr in zip(numbers[:-1], numbers[1:]):
        if prev - curr <= 0:
            return False
    return True


def analyze_report_old(
    report: list[int], length: int, dampener: bool = False, memory: dict[tuple[int], bool] = {}
) -> bool:
    """
    This function analyze a report and mark if safe/unsafe based on these criteria
    1. Report must be either in increasing or decreasing order
    2. Adjacent values must be between the distance [1, 3] both inclusive
    :param report: list of int, levels measured in a report
    :param length: int, length of the report, i.e. number of levels in the report
    :param dampener: bool, by default False, but if True - fault in one of the levels is tolerated
    :param memory: dict, a hashmap of report and its result
    :return: bool, True if report obeys above criteria False otherwise
    """
    if length - len(report) > 1:
        return False

    level_difference = [y - x for x, y in zip(report[:-1], report[1:])]
    sign_dict = defaultdict(int)
    sign_dict["neg"] = sum(map(lambda x: x < 0, level_difference))
    sign_dict["pos"] = sum(map(lambda x: x > 0, level_difference))
    sign_dict["zeros"] = sum(map(lambda x: x == 0, level_difference))

    print(f"{report}, {sign_dict}, {level_difference}")


def analyst_report_deprecated(report, length, dampener=True, memory={}) -> bool:
    level_difference = [(y - x) for x, y in zip(report[:-1], report[1:])]
    # increasing levels
    if any(map(lambda x: x > 0, level_difference)) > 0:
        # check all level differences are within limits of [1, 3]
        result_increasing = list(map(lambda x: 1 <= x <= 3, level_difference))
        # if dampener is False - part 1: return True only if all differences are within the limits - increasing
        # if dampener is True - part 2: return True only if all differences are within the limits - increasing or decreasing
        result = all(result_increasing)
        if result:
            return True
        else:
            new_report_left = tuple(compress(report, [True] + result_increasing))
            new_report_right = tuple(compress(report, result_increasing + [True]))

            if len(new_report_left) + 1 == length:
                memory[new_report_left] = False
                result_left = analyze_report(new_report_left, length, True, memory)
                memory[new_report_left] = memory.get(new_report_left) or result_left
                return result_left

            if len(new_report_right) + 1 == length:
                memory[new_report_right] = False
                result_right = analyze_report(new_report_right, length, True, memory)
                memory[new_report_right] = memory.get(new_report_right) or result_right
                return result_right
            print(memory)
            return False

    # decreasing levels
    else:
        # check all level differences are within limits of [-1, -3]
        result_decreasing = list(map(lambda x: -3 <= x <= -1, level_difference))
        # if dampener is False - part 1: return True only if all differences are within the limits - decreasing
        # if dampener is True - part 2: return True only if all differences are within the limits - increasing or decreasing
        result = all(result_decreasing)
        if result:
            return result
        else:
            new_report_left = tuple(compress(report, [True] + result_decreasing))
            new_report_right = tuple(compress(report, result_decreasing + [True]))
            result_left, result_right = False, False

            if len(new_report_left) + 1 == length:
                memory[new_report_left] = False
                result_left = analyze_report(new_report_left, length, True, memory)
                memory[new_report_left] = memory.get(new_report_left) or result_left
                return result_left

            if len(new_report_right) + 1 == length:
                memory[new_report_right] = False
                result_right = analyze_report(new_report_right, length, True, memory)
                memory[new_report_right] = memory.get(new_report_right) or result_right
                return result_right
            print(memory)
            return False


if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()
    print(f"Perf Counter: {(end - start) * 10 ** 3} ms")

    # associated_report([78, 81, 78, 80, 81, 83, 85, 83])
    # print(is_inc_dec([78, 81, 78, 80, 81, 83, 85, 83], len([78, 81, 78, 80, 81, 83, 85, 83]), True))
    # print(is_diff([78, 81, 78, 80, 81, 83, 85, 83], True))
    # print(is_inc_dec([1, 3, 2, 4, 5], len([1, 3, 2, 4, 5]), True))
    # print(is_diff([1, 3, 2, 4, 5], True))
