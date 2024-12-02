from typing import List
from pathlib import Path


def main():
    # file_name = Path(__file__).parent.joinpath("sample.txt")
    file_name = Path(__file__).parent.joinpath("input.txt")
    lines = get_lines(file_name)

    total = 0
    for line in lines:
        new_number = get_new_number(line, False)
        total += new_number

    print(f"Total: {total}")
    return None


def get_new_number(line: List[int], need_last_number) -> int:
    if all(number == 0 for number in line):
        return 0

    new_number = get_new_number(list(b - a for a, b in zip(line[:-1], line[1:])), need_last_number)
    return line[-1] + new_number if need_last_number else line[0] - new_number


def get_lines(file_name: str):
    lines = list()
    with open(file_name) as f:
        for line in f:
            numbers = list(map(int, line.strip().split()))
            lines.append(numbers)
    return lines



if __name__ == "__main__":
    main()
