from pathlib import Path


def main():
    file_path: str = Path(__file__).parent.joinpath('1_1_input.txt')
    lines = get_file_data(file_path)
    lines_digits = list(get_first_last_digits(line) for line in lines)
    digits = list(map(lambda x: x[0] * 10 + x[1], lines_digits))
    total = sum(digits)
    print(f"Total: {total}")
    return total


def get_first_last_digits(data: str) -> [int, int]:
    result: list = list()

    for element in data:
        if element.isdigit():
            result.append(int(element))

    return [result[0], result[-1]]


def get_file_data(file_path: str) -> str:
    result: list = list()
    with open(file_path, 'r') as file:
        return file.readlines()


if __name__ == '__main__':
    main()
