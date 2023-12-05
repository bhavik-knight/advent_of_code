import re
from pathlib import Path
from typing import List


def main():
    # file_path = Path(__file__).parent.joinpath("4_1_sample.txt")
    file_path = Path(__file__).parent.joinpath("4_1_input.txt")
    lines = get_lines(file_path)

    number_of_matching_cards_list = list(get_matching_cards(line) for line in lines)
    print(number_of_matching_cards_list)

    # part 1
    score_list = list(map(lambda x: 2 ** (x - 1) if x else 0, number_of_matching_cards_list))
    print(f"Total: {sum(score_list)}")

    # part 2
    num_of_cards = [1 for _ in range(len(lines))]
    for i, match in enumerate(number_of_matching_cards_list):
        index = 1
        # for each match, we must add to next <match> number of cards
        while index <= match:
            # total cards = original number + winning cards (for match)
            num_of_cards[i + index] += num_of_cards[i]
            index += 1

    print(num_of_cards)
    print(f"Total: {sum(num_of_cards)}")
    return None


def get_matching_cards(data: str) -> int:
    # print(f"Card: {card}")
    # get the winning set and the user's set from the data
    _, winning_set, user_set = re.split(r"[:|]", data)

    winning_set = set(map(lambda x: int(x), winning_set.strip().split()))
    user_set = set(map(lambda x: int(x), user_set.strip().split()))

    # find the matching cards
    matched_cards = winning_set.intersection(user_set)
    return len(matched_cards)


def get_lines(file_path: str) -> List[str]:
    with open(file_path, "r") as f:
        return f.readlines()


if __name__ == "__main__":
    main()
