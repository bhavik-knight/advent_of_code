from typing import List
from pathlib import Path


def main():
    # file_path = Path(__file__).parent.joinpath("sample.txt")
    file_path = Path(__file__).parent.joinpath("input.txt")
    lines = get_lines(file_path)

    total = 0.0
    new_number_list = list()
    for line in lines:
        new_number = get_new_number(line)
        print(f"{line} -> {new_number}")
        new_number_list.append(new_number)
        total += new_number

    print(f"total: {total}")
    print(f"new number list: {new_number_list}\n -> {sum(new_number_list)}")
    return None


def get_new_number(numbers: int) -> int:
    print("=" * 80)
    result = numbers[:]
    intermediate_lines = list()

    # generate lines till 0
    while sum(result) != 0:
        new_line = list()
        for n1, n2 in zip(result[:-1], result[1:]):
            new_line.append(n2 - n1)

        intermediate_lines.insert(0, new_line)
        result = new_line

    # process to generate next number
    current_last = 0
    for i, line in enumerate(intermediate_lines[1:], 1):
        current_last = line[-1] + intermediate_lines[i - 1][-1]
        line.append(current_last)
        print(line)
    print("-" * 80)

    return numbers[-1] + current_last


def get_lines(file_name: str) -> List[List[int]]:
    data = list()
    with open(file_name, "r") as f:
        for line in f:
            numbers = list(map(int, line.strip().split()))
            data.append(numbers)
    return data


if __name__ == "__main__":
    main()
