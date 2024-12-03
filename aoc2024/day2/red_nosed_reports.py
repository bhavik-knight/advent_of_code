"""
AOC 2024
Day 2 : Red-Nosed Reports
Coded by: Bhavik Knight
"""

from time import perf_counter


def main():
    files = ["test_input.txt", "input.txt"]

    for file in files:
        print("=" * 80)
        print(f"File: {file}")
        reports = parse_input(file)

        total_part1, total_part2 = 0, 0
        memory: dict[tuple, bool] = {}

        for i, report in enumerate(reports, 1):
            result_part1 = analyze_report(report, dampener=False, memory=memory)
            # print(f"Part1: Report[{i}]: => {report} -> {result_part1}")
            total_part1 += int(result_part1)
            memory[tuple(report)] = result_part1

        print("-" * 50)

        # these are stored in memory already
        skipped_reports = 0
        for i, report in enumerate(reports, 1):
            if memory.get(tuple(report)):
                total_part2 += 1
                skipped_reports += 1
                continue

            result_part2 = analyze_report(report, dampener=True, memory=memory)
            # print(f"Part2: Report[{i + skipped_reports}]: => {report} -> {result_part2}")
            total_part2 += int(result_part2)
            memory[tuple(report)] = result_part2

        print("-" * 50)
        print(f"Total Part1: {total_part1}")
        print(f"Total Part2: {total_part2}")

        print("=" * 80)


def analyze_report(report: list[int], dampener: bool = False, memory: dict[tuple, bool] = {}) -> bool:
    # without dampener there isn't any tolerance however
    if not dampener:
        result_difference = condition_difference(report)
        result_int_dec = condition_monotonic(report)
        combined_result = result_difference and result_int_dec
        # print(f"Report: {report}, RD: {result_difference}, RID: {result_int_dec} ==> {combined_result}")
        memory[tuple(report)] = combined_result
        return combined_result

    # dampener allows at most one tolerance
    result_associated_reports: dict[tuple, bool] = {}
    # check all associated reports
    for report in get_associate_report(report):
        level_difference = get_level_difference(report)
        tolerance_counter = get_tolerance_count(level_difference)
        nc, pc, zc = get_counts(level_difference)

        # if both negative_counts, and positive counts are more than 1
        # or zero counts are more than 1
        # then report is not monotonic - strictly increasing/decreasing

        # if tolerance_counter is more than 0
        # levels in the report are not in the expected range [1, 3]
        if nc > 1 and pc > 0 or zc > 0 or nc > 0 and pc > 1 or zc > 0 or tolerance_counter > 0:
            result_associated_reports[tuple(report)] = False
        else:
            result_associated_reports[tuple(report)] = True

    # the result of dampener which allows tolerance of 1
    dampener_result = any(result_associated_reports.values())
    memory[tuple(report)] = dampener_result
    return dampener_result


def parse_input(file_name: str) -> list[list[int]]:
    with open(file_name, "r") as f:
        lines = [line.strip() for line in f.readlines()]
    return [[int(x) for x in line.split()] for line in lines]


def get_level_difference(numbers: list[int]) -> list[int]:
    return list(y - x for x, y in zip(numbers[:-1], numbers[1:]))


def get_tolerance_count(numbers: list[int]) -> int:
    return sum(map(lambda x: not 1 <= abs(x) <= 3, numbers))


def condition_difference(report: list[int]) -> bool:
    level_difference = get_level_difference(report)
    tolerance_count = get_tolerance_count(level_difference)
    return tolerance_count == 0


def get_counts(numbers: list[int]) -> tuple[int, int, int]:
    negative_count = sum(map(lambda x: x < 0, numbers))
    positive_count = sum(map(lambda x: x > 0, numbers))
    zero_count = sum(map(lambda x: x == 0, numbers))
    return negative_count, positive_count, zero_count


def condition_monotonic(report: list[int]) -> bool:
    level_difference = get_level_difference(report)
    negative_count, positive_count, zero_count = get_counts(level_difference)

    if (negative_count >= 1 and positive_count >= 1) or zero_count > 0:
        return False

    if (negative_count >= 1 and positive_count == 0 and zero_count == 0) or \
            (negative_count == 0 and positive_count >= 1 and zero_count == 0):
        return True


def get_associate_report(report: list[int]) -> list[list[int]]:
    return [report[:i] + report[i + 1:] for i in range(len(report))]


if __name__ == "__main__":
    start_pc = perf_counter()
    main()
    end_pc = perf_counter()
    print(f"Time taken: {(end_pc - start_pc) * 10 ** 3} ms")
