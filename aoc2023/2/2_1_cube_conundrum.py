from itertools import accumulate
from operator import mul
from pathlib import Path


def main():
    # criteria to determine if a game is possible
    # Red: 12, Green: 13, Blue: 14 - max possible cubes can be picked in a set
    criteria = [12, 13, 14]

    # path of input file
    file_path = Path(__file__).parent.joinpath("2_0_sample_input.txt")
    file_path = Path(__file__).parent.joinpath("2_1_input.txt")

    # get all the lines
    lines = get_input(file_path)

    # get data of each game: game_number -> [red, green, blue]
    games: dict = dict()
    for line in lines:
        game = get_game_data(line)
        games.update(game)
    # print(f"games: {games}")

    # result of each game
    games_result = {game_number: is_game_possible(game_data, criteria) for game_number, game_data in games.items()}

    result = sum(k * v for k, v in games_result.items())
    print(f"desired_sum: {result}")

    # 2_2 - sum of power of each game sets
    sum_of_multiplications = sum(list(accumulate(v, mul))[-1] for v in games.values())
    print(f"sum_of_multiplications: {sum_of_multiplications}")
    return result


def is_game_possible(data: list, criteria: list) -> bool:
    return all(trial <= rule for trial, rule in zip(data, criteria))


def get_game_data(data: str) -> dict:
    game, cube_sets = data.split(":")

    # a set represents number of Red, Green, and Blue cubes respectively in a set
    rgb_set = [0, 0, 0]
    for cube_set in cube_sets.split(";"):
        # print(f"cube_set: {cube_set}")

        # a set is the different color of cubes picked at a time
        # go over different color of cubes picked in this set at this time
        for a_set in cube_set.split(","):
            # number and color of cubes picked during this set
            number, color = a_set.split()

            # record the maximum number of cube picked in a trial for each color until this trial
            if color == "red":
                rgb_set[0] = max(rgb_set[0], int(number))
            elif color == "green":
                rgb_set[1] = max(rgb_set[1], int(number))
            else:
                rgb_set[2] = max(rgb_set[2], int(number))

    game_number = int(game.split()[-1])
    return {game_number: rgb_set}


def get_input(file_path: str) -> list:
    with open(file_path, "r") as file:
        lines = file.readlines()
    return lines


if __name__ == "__main__":
    main()
