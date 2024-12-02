import re, math
from pathlib import Path


def main():
    # file_path = Path(__file__).parent.joinpath("6_sample.txt")
    file_path = Path(__file__).parent.joinpath("6_input.txt")

    boat_data = get_data(file_path)
    print(f"Boat: {boat_data}")

    num_win_ways_list = list()
    for time, distance in boat_data.items():
        num_win_ways_list.append(get_num_win_ways(time, distance))

    print(num_win_ways_list)
    print(f"puzzle 1: {math.prod(num_win_ways_list)}")

    print(alt_win_ways())
    return None


def get_num_win_ways(time, distance):
    t = time // 2
    result = 0

    while t * (time - t) > distance:
        result += 2
        t -= 1
    return result if time % 2 else result - 1


def alt_win_ways(time = 30, distance = 200):
    start, end = 0, time
    mid_record = dict()
    while start < end:
        mid = (end - start) // 2 + start // 2
        if mid * (time - mid) > distance:
            mid_record[mid] = True
            end = mid - 1
        else:
            mid_record[mid] = False
            start = mid + 1
    print(mid_record)
    return mid_record


def get_data(file_name: str, round_two: bool = True) -> dict:
    times, distances = None, None
    with open(file_name, "r") as f:
        for line in f:
            if line.startswith("Time"):
                _, times = line.strip().split(":")
                if round_two:
                    time = int("".join(map(str, times.split())))
                else:
                    times = list(map(int, times.split()))
            else:
                _, distances = line.strip().split(":")
                if round_two:
                    distance = int("".join(map(str, distances.split())))
                else:
                    distances = list(map(int, distances.split()))

                # print(f"Distances: {distances}, {type(distances[0])}, {distances[0]}")

    boat_data = {time: distance} if round_two else dict(zip(times, distances))
    return boat_data


if __name__ == "__main__":
    main()
