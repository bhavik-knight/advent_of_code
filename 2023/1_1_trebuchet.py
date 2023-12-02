from pathlib import Path


def main():
    # path of input file
    file_path: str = Path(__file__).parent.joinpath("1_1_input.txt")

    # get all the lines
    lines = get_file_data(file_path)

    # the digits in the first and last position of each line
    lines_digits = list(get_first_last_digits(line) for line in lines)

    # convert two digits into a 2-digit number
    digits = list(map(lambda x: x[0] * 10 + x[1], lines_digits))

    # sum of all the 2-digit numbers
    total = sum(digits)
    print(f"Total: {total}")

    return total


def get_first_last_digits(data: str) -> [int, int]:
    result = [int(element) for element in data if element.isdigit()]
    return [result[0], result[-1]]


def get_file_data(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.readlines()


if __name__ == "__main__":
    main()
