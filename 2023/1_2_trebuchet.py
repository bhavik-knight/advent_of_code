import sys
from pathlib import Path


def main():
    # book-keeping
    mapping_dict: dict = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }


    # get the file path
    file_path: str = Path(__file__).parent.joinpath('1_1_input.txt')

    # get all lines from the file
    lines = get_file_data(file_path)

    # get first and last digits from each line
    lines_digits = list(get_first_last_digits(line, mapping_dict) for line in lines)

    # convert the above list to a list of two digit numbers
    digits = list(map(lambda x: x[0] * 10 + x[1], lines_digits))

    for line, digit in zip(lines, digits):
        print(f"{line.strip():50}\t->\t{digit}")

    # find the sum
    total = sum(digits)
    print(f"Total: {total}")

    return total


def get_first_last_digits(data: str, mapping_dict: dict) -> [int, int]:
    # mapping digit to the position in the data
    result: dict = dict()

    # first create a dictionary with all values as empty lists for the positions
    for word in mapping_dict:
        result[mapping_dict[word]] = list()

    # capture the digits encoded as words in the data
    for word in mapping_dict:
        try:
            # find both left and right position of the word in the data
            left_position: int = data.index(word)
            right_position: int = data.rindex(word)
        except ValueError:
            continue
        else:
            # if both positions are same, then the word is present only once
            if left_position == right_position:
                result[mapping_dict[word]].append(left_position)
            else:
                result[mapping_dict[word]].extend([left_position, right_position])

    # capture the digits encoded as digits themselves
    for i, element in enumerate(data):
        if element.isdigit():
            result[int(element)].append(i)

    # transform the dictionary
    # remove the empty lists entries as values from the dictionary
    # also sort the list of values for each key
    result_removed_empty = {key: sorted(value) for key, value in result.items() if value}
    print(data, result_removed_empty)

    first_position, first_digit = sys.maxsize, None
    for d, positions in result_removed_empty.items():
        min_position = min(positions)
        if min_position < first_position:
            first_position = min_position
            first_digit = d
    print(f"first: {first_digit, first_position}")

    last_position, last_digit = -sys.maxsize, None
    for d, positions in result_removed_empty.items():
        max_position = max(positions)
        if max_position > last_position:
            last_position = max_position
            last_digit = d
    print(f"last: {last_digit, last_position}")

    print("-" * 80)
    return [first_digit, last_digit]


def get_file_data(file_path: str) -> str:
    result: list = list()
    with open(file_path, 'r') as file:
        return file.readlines()


if __name__ == '__main__':
    main()
