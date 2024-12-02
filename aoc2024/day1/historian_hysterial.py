"""
AOC Day1: Historian Hysteria
Coded by: Bhavik Knight
"""

from collections import Counter


def main():
    """
    The main function to run the program
    Returns: None
    """

    # input_files = ["test_input.txt"]
    input_files = ["test_input.txt", "input.txt"]

    for file in input_files:
        locations = parse_input(file)
        distance = get_total_distance(locations)
        print(f"Total Distance: {distance}")

        similarity_score = get_similarity_score(locations)
        print(f"Similarity score: {similarity_score}")


def parse_input(file_name: str) -> list[list[int], list[int]]:
    """
    This function parse the user's input from the file
    Returns: list, a list of two lists of integers
    """

    # open file and read lines
    with open(file_name, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    # split each line based on spaces between them
    result = list(map(lambda x: x.split(), lines))

    # transpost this list so that we can have a two lists of integers
    transpose = zip(*map(lambda x: [int(x[0]), int(x[1])], result))
    return list(transpose)


def get_total_distance(location_list: list[list[int], list[int]]) -> int:
    """
    This function counts the sum of differences between pair of locations
    Returns: int, the total distance
    """
    location_x, location_y = [sorted(x) for x in location_list]
    # print(location_x, location_y)
    return sum(abs(x - y) for x, y in zip(location_x, location_y))


def get_similarity_score(location_list: list[list[int], list[int]]) -> int:
    """
    This function generates a similarity score.
    1. Counts the frequency of a number in the list1 from list2.
        Number 3 is in the list1, appears 5 times in the list2
        Number 2 is in the list1, appears 2 times in the list2
    2. Similarity score = 3 * 5 + 2 * 2 = 15 + 4 = 19

    Returns: int, similarity score
    """

    location_x, location_y = list(location_list)
    # print(f"Location X: {location_x}, {Counter(location_x)}")

    # counts the number of times a number appear in the location_x
    frequency_count: dict[int, int] = Counter(location_x)

    # update the freqeuency count according to the number of times a number appears in location_y
    for number, count in frequency_count.items():
        frequency_count[number] = count * location_y.count(number)

    # print(frequency_count)
    similarity_score = sum(k * v for k, v in frequency_count.items())
    return similarity_score


if __name__ == "__main__":
    main()
