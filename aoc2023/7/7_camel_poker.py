from typing import List
from pathlib import Path


def main():
    # file_path = Path(__file__).parent.joinpath("sample.txt")
    # file_path = Path(__file__).parent.joinpath("test.txt")
    file_path = Path(__file__).parent.joinpath("input.txt")
    all_bids = dict()

    converted_hands_mapping = dict()

    high_cards, converted_high_cards = list(), list()
    one_pairs, converted_one_pairs = list(), list()
    two_pairs, converted_two_pairs = list(), list()
    three_of_a_kinds, converted_three_of_a_kinds = list(), list()
    full_houses, converted_full_houses = list(), list()
    four_of_a_kinds, converted_four_of_a_kinds = list(), list()
    five_of_a_kinds, converted_five_of_a_kinds = list(), list()

    with open(file_path, "r") as f:
        for line in f:
            hand, bid = line.strip().split()
            all_bids[hand] = int(bid)

            # puzzle 1
            hand_name = get_hand(hand)
            match hand_name:
                case "High card":
                    high_cards.append(hand)
                case "One pair":
                    one_pairs.append(hand)
                case "Two pair":
                    two_pairs.append(hand)
                case "Three of a kind":
                    three_of_a_kinds.append(hand)
                case "Full house":
                    full_houses.append(hand)
                case "Four of a kind":
                    four_of_a_kinds.append(hand)
                case "Five of a kind":
                    five_of_a_kinds.append(hand)

            # puzzle 2
            converted_hand = convert_to_best(hand)
            match get_hand(converted_hand):
                case "High card":
                    converted_high_cards.append((hand, converted_hand))
                    converted_hands_mapping[hand] = converted_hand
                case "One pair":
                    converted_one_pairs.append((hand, converted_hand))
                    converted_hands_mapping[hand] = converted_hand
                case "Two pair":
                    converted_two_pairs.append((hand, converted_hand))
                    converted_hands_mapping[hand] = converted_hand
                case "Three of a kind":
                    converted_three_of_a_kinds.append((hand, converted_hand))
                    converted_hands_mapping[hand] = converted_hand
                case "Full house":
                    converted_full_houses.append((hand, converted_hand))
                    converted_hands_mapping[hand] = converted_hand
                case "Four of a kind":
                    converted_four_of_a_kinds.append((hand, converted_hand))
                    converted_hands_mapping[hand] = converted_hand
                case "Five of a kind":
                    converted_five_of_a_kinds.append((hand, converted_hand))
                    converted_hands_mapping[hand] = converted_hand


    # puzzle 1
    different_hands = [
        sort_hands(hands) for hands in [
            high_cards,
            one_pairs,
            two_pairs,
            three_of_a_kinds,
            full_houses,
            four_of_a_kinds,
            five_of_a_kinds
        ]
    ]

    rank = 1
    all_wins = dict()
    # find the actual win of each hand according to the rank
    for hands in different_hands:
        for hand in hands:
            all_wins[hand] = (rank, rank * all_bids[hand])
            rank += 1

    total = 0
    for hand, (rank, winning) in all_wins.items():
        print(hand, rank, winning)
        total += winning
    print(f"total wins: {total}")
    print(f"\n\n\n\n")


    # puzzle 2
    different_converted_hands = [
        sort_hands(hands, True) for hands in [
            converted_high_cards,
            converted_one_pairs,
            converted_two_pairs,
            converted_three_of_a_kinds,
            converted_full_houses,
            converted_four_of_a_kinds,
            converted_five_of_a_kinds
        ]
    ]

    # for hands in different_converted_hands:
        # for hand in hands:
            # print(hand)
        # print("-" * 80)

    converted_rank = 1
    all_converted_wins = dict()

    # find the actual win of each hand according to the rank
    for hands in different_converted_hands:
        for hand in hands:
            # original_hand = list(filter(lambda x: x[1], ((check_hand, hand == converted_hands_mapping[check_hand]) for check_hand in converted_hands_mapping)))[0][0]
            all_converted_wins[hand] = (converted_rank, converted_rank * all_bids[hand])
            converted_rank += 1

    print("All_converted_wins", len(all_converted_wins))
    converted_total = 0
    for hand, (rank, winning) in all_converted_wins.items():
        print("Converted:", hand, rank, winning)
        converted_total += winning
    print(f"total wins: {converted_total}")

    return None


def sort_hands(hands: List[str], joker=False) -> List[str]:
    ranks = {"2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7, "9": 8, "T": 9, "J": 10, "Q": 11, "K": 12, "A": 13}
    if joker:
        ranks = {"J": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
                    "7": 7, "8": 8, "9": 9, "T": 10, "Q": 11, "K": 12, "A": 13}

    new_hands = dict()
    for hand in hands:
        if joker:
            hand, converted_hand = hand
            hand_order = list(ranks[card] * i for i, card in enumerate(converted_hand, 1))
        hand_order = list(ranks[card] * i for i, card in enumerate(hand, 1))
        new_hands[hand] = hand_order

    sorted_hands = sorted(new_hands, key=new_hands.get)
    print("sorted hands", sorted_hands)
    return sorted_hands


def convert_to_best(hand: str) -> str:
    ranks = {"2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7, "9": 8, "T": 9, "J": 10, "Q": 11, "K": 12, "A": 13}
    hand_dict = dict()
    for card in hand:
        if card != "J":
            hand_dict[card] = hand_dict.get(card, 0) + 1

    hand_dict = {card: [hand_dict[card], ranks[card]] for card in hand_dict}
    sorted_hand = sorted(
            ((k, v) for k, v in hand_dict.items()),
            key=lambda x: (-x[1][0], -x[1][1])
        )

    converted_hand = hand.replace("J", sorted_hand[0][0]) if sorted_hand else hand
    # print(">>>", hand, converted_hand)
    return converted_hand


def get_hand(hand: str) -> str:
    hand_dict = {card: hand.count(card) for card in hand}
    matches = max(hand_dict.values())
    match matches:
        case 1:
            return "High card"
        case 2:
            return "Two pair" if len(hand_dict) == 3 else "One pair"
        case 3:
            return "Three of a kind" if len(hand_dict) == 3 else "Full house"
        case 4:
            return "Four of a kind"
        case 5:
            return "Five of a kind"


if __name__ == "__main__":
    main()
